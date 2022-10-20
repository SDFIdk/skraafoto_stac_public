"""Item crud client."""
import json
import logging
import operator
from datetime import datetime
from typing import List, Optional, Set, Type, Union, Dict, Any
from urllib.parse import urlencode, urljoin

import attr
import geoalchemy2 as ga
import sqlalchemy as sa
from sqlalchemy.sql.expression import true, tuple_
from sqlalchemy import and_
import stac_pydantic
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from shapely.geometry import Polygon as ShapelyPolygon
from shapely.geometry import shape
from sqlakeyset import get_page
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import array
from sqlalchemy.orm import Session as SqlSession, with_expression
from stac_pydantic.links import Relations
from stac_pydantic.shared import MimeTypes, BBox

from stac_fastapi.sqlalchemy import serializers
from stac_fastapi.sqlalchemy.models import database
from stac_fastapi.sqlalchemy.session import Session
from stac_fastapi.sqlalchemy.pagination import PaginationTokenClient
from stac_fastapi.sqlalchemy.types.search import (
    STACSearch,
    Queryables,
)
from stac_fastapi.types.config import Settings
from stac_fastapi.types.core import BaseCoreClient, BaseFiltersClient
from stac_fastapi.sqlalchemy.types.search import Queryables
from stac_fastapi.sqlalchemy.types.links import ApiTokenHrefBuilder
from stac_fastapi.sqlalchemy.config import QueryableInfo, SqlalchemySettings
from stac_fastapi.types.errors import NotFoundError
from stac_fastapi.types.links import BaseHrefBuilder
from stac_fastapi.types.stac import Collection, Collections, Item, ItemCollection
from pygeofilter.backends.sqlalchemy import to_filter
import pygeofilter
from pygeoif.geometry import as_shape

NumType = Union[float, int]

import cProfile
import io
import pstats
import contextlib

@contextlib.contextmanager
def profiled():
    pr = cProfile.Profile()
    pr.enable()
    yield
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
    ps.print_stats()
    # uncomment this to see who's calling what
    # ps.print_callers()
    print(s.getvalue())

def monkeypatch_parse_geometry(geom):
    wkt = as_shape(geom).to_wkt()
    crs = geom["crs"] if "crs" in geom.keys() else 4326
    if crs == 4326:
        return func.ST_GeomFromText(wkt, 4326)
    else:
        return func.ST_Transform(func.ST_GeomFromText(wkt, crs), 4326)


@attr.s
class CoreCrudClient(PaginationTokenClient, BaseCoreClient):
    """Client for core endpoints defined by stac."""

    session: Session = attr.ib(default=attr.Factory(Session.create_from_env))
    item_table: Type[database.ImageView] = attr.ib(default=database.ImageView)
    collection_table: Type[database.Collection] = attr.ib(default=database.Collection)
    item_serializer: Type[serializers.Serializer] = attr.ib(
        default=serializers.ItemSerializer
    )
    collection_serializer: Type[serializers.Serializer] = attr.ib(
        default=serializers.CollectionSerializer
    )
    storage_srid: int = attr.ib(default=4326)

    FIELD_MAPPING = {}
    for q in Queryables.get_all_queryables():
        FIELD_MAPPING[q] = item_table._default.get_field(q)

    @staticmethod
    def _lookup_id(
        id: str,
        table: Type[database.BaseModel],
        session: SqlSession,
        query_options: Any = [],
        collection_id: str = None,
    ) -> Type[database.BaseModel]:
        """Lookup row by id."""
        if collection_id:
            _filter = and_(table.id == id, collection_id == table.collection_id)
        else:
            _filter = table.id == id
        row = session.query(table).options(query_options).filter(_filter).first()
        if not row:
            raise NotFoundError("Not found")
        return row

    def _geometry_expression(self, to_srid: int):
        """Returns Ad Hoc SQL expression which can be applied to a "deferred expression" attribute.
        The expression makes sure the geometry is returned in the requested SRID."""
        if to_srid != self.storage_srid:
            geom = ga.func.ST_Transform(self.item_table.footprint, to_srid)
        else:
            geom = self.item_table.footprint

        return with_expression(
            self.item_table.footprint,
            geom,
        )

    def _bbox_expression(self, to_srid: int):
        """Returns Ad Hoc SQL expression which can be applied to a "deferred expression" attribute.
        The expression makes sure the BBOX is returned in the requested SRID."""
        if to_srid != self.storage_srid:
            geom = ga.func.ST_Transform(self.item_table.footprint, to_srid)
        else:
            geom = self.item_table.footprint

        return with_expression(
            self.item_table.bbox,
            array(
                [
                    ga.func.ST_XMin(ga.func.ST_Envelope(geom)),
                    ga.func.ST_YMin(ga.func.ST_Envelope(geom)),
                    ga.func.ST_XMax(ga.func.ST_Envelope(geom)),
                    ga.func.ST_YMax(ga.func.ST_Envelope(geom)),
                ]
            ),
        )

    def create_crs_response(self, resp, crs, **kwargs) -> JSONResponse:
        """Add Content-Crs header to JSONResponse to comply with OGC API Feat part 2"""
        crs_ext = self.get_extension("CrsExtension")
        if crs is None:
            crs = crs_ext.storageCrs
        if crs in crs_ext.crs:  # If the CRS is valid
            return JSONResponse(resp, headers={"Content-Crs": crs})
        else:
            return resp

    def href_builder(self, **kwargs) -> BaseHrefBuilder:
        """Override with HrefBuilder which adds API token to all hrefs if present"""
        request = kwargs["request"]
        base_url = str(request.base_url)
        token = request.query_params.get("token")
        return ApiTokenHrefBuilder(base_url, token)

    def all_collections(self, **kwargs) -> Collections:
        """Read all collections from the database."""
        hrefbuilder = self.href_builder(**kwargs)
        with self.session.session_maker.context_session() as session:
            collections = session.query(self.collection_table).all()
            serialized_collections = [
                self.collection_serializer.db_to_stac(collection, hrefbuilder)
                for collection in collections
            ]
            # TODO: incorporate this into the serializer perhaps
            if self.extension_is_enabled("CrsExtension"):
                for c in serialized_collections:
                    c.update({"crs": self.get_extension("CrsExtension").crs})

            links = [
                {
                    "rel": Relations.root.value,
                    "type": MimeTypes.json,
                    "href": hrefbuilder.build("./"),
                },
                {
                    "rel": Relations.parent.value,
                    "type": MimeTypes.json,
                    "href": hrefbuilder.build("./"),
                },
                {
                    "rel": Relations.self.value,
                    "type": MimeTypes.json,
                    "href": hrefbuilder.build("./collections"),
                },
            ]
            collection_list = Collections(
                collections=serialized_collections or [], links=links
            )
            return collection_list

    def get_collection(self, id: str, **kwargs) -> Collection:
        """Get collection by id."""
        hrefbuilder = self.href_builder(**kwargs)
        with self.session.session_maker.context_session() as session:
            collection = self._lookup_id(id, self.collection_table, session)  #

            serialized_collection = self.collection_serializer.db_to_stac(
                collection, hrefbuilder
            )
            # Add the list of service supported CRS to the collection
            if self.extension_is_enabled("CrsExtension"):
                serialized_collection.update(
                    {"crs": self.get_extension("CrsExtension").crs}
                )
            return serialized_collection

    def item_collection(
        self,
        id: str,
        ids: Optional[List[str]] = None,
        bbox: str = None,
        bbox_crs: str = None,
        datetime: Optional[Union[str, datetime]] = None,
        crs: Optional[str] = None,
        filter: Optional[str] = None,
        filter_lang: Optional[str] = "cql-json",
        filter_crs: Optional[str] = "http://www.opengis.net/def/crs/OGC/1.3/CRS84",
        limit: int = 10,
        pt: str = None,
        **kwargs,
    ) -> ItemCollection:
        """Get items by collection"""
        # Do the request
        base_args = {
            "collections": [id],
            "ids": ids,
            "limit": limit,
            "pt": pt,
            "filter": None,
            "filter": filter,
            "filter_lang": filter_lang,
            "filter_crs": filter_crs,
            # "query": None,
        }
        # TODO: just add these in and filter out the None values later
        if datetime:
            base_args["datetime"] = datetime
        if bbox_crs is not None:
            # TODO move into the validator, once it's figured out how to reference the CRS extension
            if self.get_extension("CrsExtension").is_crs_supported(bbox_crs):
                base_args["bbox_crs"] = bbox_crs
            else:
                raise HTTPException(
                    status_code=400,
                    detail="CRS provided for argument bbox_crs is invalid, valid options are: "
                    + ",".join(self.get_extension("CrsExtension").crs),
                )
        if bbox:
            base_args["bbox"] = tuple(map(float, bbox.split(",")))
        if crs:
            if self.get_extension("CrsExtension").is_crs_supported(crs):
                base_args["crs"] = crs
            else:
                raise HTTPException(
                    status_code=400,
                    detail="CRS provided for argument crs is invalid, valid options are: "
                    + ",".join(self.get_extension("CrsExtension").crs),
                )

        try:
            search_request = STACSearch(**base_args)
        except ValidationError:
            raise HTTPException(status_code=400, detail="Invalid parameters provided")
        resp = self.post_search(search_request, False, request=kwargs["request"])

        # If we get 0 features it may be because the collection id does not exist. We should return 404
        if len(resp["features"]) == 0:
            # this raises a NotFound error if collection id does not exist
            with self.session.session_maker.context_session() as session:
                self._lookup_id(id, self.collection_table, session)

        # Pagination
        hrefbuilder = self.href_builder(**kwargs)
        page_links = []
        for link in resp["links"]:
            if (
                link["rel"] == Relations.next
                or link["rel"] == Relations.previous
                or link["rel"] == Relations.self
            ):
                query_params = dict(kwargs["request"].query_params)
                if link["body"]:
                    query_params.update(link["body"])
                if not "limit" in query_params:
                    query_params.update({"limit": limit})
                link["method"] = "GET"
                link["href"] = hrefbuilder.build(
                    f"collections/{id}/items", query_params
                )
                link.pop("body", None) # body only relevant for POST
                page_links.append(link)
            else:
                page_links.append(link)
        resp["links"] = page_links

        # ItemCollection
        if self.extension_is_enabled("CrsExtension"):
            return self.create_crs_response(resp, crs)

        return resp

    def get_item(self, item_id: str, collection_id: str, **kwargs) -> Item:
        """Get item by id."""
        request = kwargs["request"]
        output_srid = 4326
        req_crs = request.query_params.get("crs")
        if req_crs and self.extension_is_enabled("CrsExtension"):
            stac_crs = self.get_extension("CrsExtension")
            if self.get_extension("CrsExtension").is_crs_supported(req_crs):
                output_srid = stac_crs.epsg_from_crs(req_crs)
            else:
                raise HTTPException(
                    status_code=400,
                    detail="CRS provided for argument crs is invalid, valid options are: "
                    + ",".join(self.get_extension("CrsExtension").crs),
                )
        else:
            req_crs = "http://www.opengis.net/def/crs/OGC/1.3/CRS84"

        hrefbuilder = self.href_builder(**kwargs)
        with self.session.session_maker.context_session() as session:
            options = (
                self._bbox_expression(output_srid),
                self._geometry_expression(output_srid),
            )

            item = self._lookup_id(
                item_id, self.item_table, session, options, collection_id=collection_id
            )
            resp = self.item_serializer.db_to_stac(item, hrefbuilder)
            if self.get_extension("CrsExtension"):
                if (
                    "crs" not in resp["properties"]
                ):  # If the CRS type has not been populated to the response
                    crs_obj = {
                        "type": "name",
                        "properties": {"name": f"{req_crs}"},
                    }
                resp["properties"]["crs"] = crs_obj
                return self.create_crs_response(resp, req_crs)

            return resp

    def get_search(
        self,
        collections: Optional[List[str]] = None,
        ids: Optional[List[str]] = None,
        bbox: Optional[List[NumType]] = None,
        bbox_crs: Optional[str] = None,
        intersects: Optional[str] = None,
        datetime: Optional[Union[str, datetime]] = None,
        limit: Optional[int] = 10,
        filter: Optional[str] = None,
        filter_lang: Optional[str] = "cql-json",
        filter_crs: Optional[str] = "http://www.opengis.net/def/crs/OGC/1.3/CRS84",
        # query: Optional[str] = None,
        pt: Optional[str] = None,
        fields: Optional[List[str]] = None,
        sortby: Optional[str] = None,
        crs: Optional[str] = None,
        **kwargs,
    ) -> ItemCollection:
        """GET search catalog."""
        # Parse request parameters

        base_args = {
            "collections": collections,
            "ids": ids,
            "bbox": bbox,
            "limit": limit,
            "filter": json.loads(filter) if filter else filter,
            "filter_lang": filter_lang or "cql-json",
            "filter_crs": filter_crs or "http://www.opengis.net/def/crs/OGC/1.3/CRS84",
            "pt": pt,
            # "query": json.loads(query) if query else query,
        }
        if crs:
            base_args["crs"] = crs
        if bbox_crs:
            base_args["bbox_crs"] = bbox_crs
        if intersects:
            base_args["intersects"] = json.loads(intersects)
        if datetime:
            base_args["datetime"] = datetime
        if sortby:
            # https://github.com/radiantearth/stac-spec/tree/master/api-spec/extensions/sort#http-get-or-post-form
            sort_param = []
            for sort in sortby:
                if (
                    sort[0] == " "
                ):  # https://www.w3.org/Addressing/URL/uri-spec.html non-urlencoded "+" signs turn into " ".
                    raise HTTPException(
                        status_code=400,
                        detail=[
                            f"Invalid parameters provided, if using + notation (+{sort[1:]}), remember to URL encode the request"
                        ],
                    )
                field = sort
                direction = "asc"  # Default behaviour
                if field[0] in ("-", "+"):
                    field = sort[1:]
                    direction = "asc" if sort[0] in ("+", " ") else "desc"

                sort_param.append(
                    {
                        "field": field,
                        "direction": direction,
                    }
                )
            base_args["sortby"] = sort_param

        if fields is not None:
            includes = set()
            excludes = set()
            for field in fields:
                if field[0] == "-":
                    excludes.add(field[1:])
                elif field[0] == "+":
                    includes.add(field[1:])
                else:
                    includes.add(field)
            base_args["fields"] = {"include": includes, "exclude": excludes}

        # Do the request
        try:
            search_request = STACSearch(**base_args)
        except ValidationError as e:
            raise HTTPException(
                status_code=400,
                detail=["Invalid parameters provided"] + str(e).split("\n"),
            )
        resp = self.post_search(search_request, False, request=kwargs["request"])

        # Pagination
        page_links = []
        hrefbuilder = self.href_builder(**kwargs)
        for link in resp["links"]:
            if (
                link["rel"] == Relations.next
                or link["rel"] == Relations.previous
                or link["rel"] == Relations.self
            ):
                query_params = dict(kwargs["request"].query_params)
                if link["body"]:
                    query_params.update(link["body"])
                link["href"] = hrefbuilder.build(f"search", query_params)
                link["method"] = "GET"
                link.pop("body", None) # Body only used for POST
                page_links.append(link)
            else:
                page_links.append(link)
        resp["links"] = page_links
        return resp

    def post_search(
        self,
        search_request: STACSearch,
        is_direct_post=True,
        **kwargs,
    ) -> ItemCollection:
        """POST search catalog."""
        with self.session.session_maker.context_session() as session:
            pagination_token = (
                self.from_token(search_request.pt) if search_request.pt else False
            )

            query = session.query(self.item_table)
            # Make sure output is in correct srids
            if (
                hasattr(search_request, "crs")
                and self.extension_is_enabled("CrsExtension")
                and search_request.crs is not None
            ):

                stac_crs = self.get_extension("CrsExtension")
                try:
                    output_srid = stac_crs.epsg_from_crs(search_request.crs)
                    output_crs = search_request.crs
                except ValueError as e:
                    raise HTTPException(
                        status_code=400,
                        detail=["Invalid parameters provided"] + str(e).split("\n"),
                    )
            else:
                output_srid = 4326
                output_crs = "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
                if self.extension_is_enabled("CrsExtension"):
                    output_crs = self.get_extension("CrsExtension").storageCrs

            # Transform footprint and bbox if necessary
            query = query.options(self._geometry_expression(output_srid))
            query = query.options(self._bbox_expression(output_srid))

            # Filter by collection
            count = None
            if search_request.collections:
                collection_id_filter = sa.or_(
                    *[
                        self.item_table.collection_id == col_id
                        for col_id in search_request.collections
                    ]
                )
                query = query.filter(collection_id_filter)

            # Ignore other parameters if ID is present
            if search_request.ids:
                id_filter = sa.or_(
                    *[self.item_table.id == i for i in search_request.ids]
                )
                items = query.filter(id_filter).order_by(self.item_table.id)
                page = get_page(
                    items, per_page=search_request.limit, page=pagination_token
                )
                if self.extension_is_enabled("ContextExtension"):
                    count = len(search_request.ids)
                page.next = (
                    self.to_token(keyset=page.paging.bookmark_next)
                    if page.paging.has_next
                    else None
                )
                page.previous = (
                    self.to_token(keyset=page.paging.bookmark_previous)
                    if page.paging.has_previous
                    else None
                )

            else:
                # Spatial query
                geom = None
                if search_request.intersects is not None:
                    geom = shape(search_request.intersects)
                elif search_request.bbox:
                    if len(search_request.bbox) == 4:
                        geom = ShapelyPolygon.from_bounds(*search_request.bbox)
                    elif len(search_request.bbox) == 6:
                        """Shapely doesn't support 3d bounding boxes we'll just use the 2d portion"""
                        bbox_2d = [
                            search_request.bbox[0],
                            search_request.bbox[1],
                            search_request.bbox[3],
                            search_request.bbox[4],
                        ]
                        geom = ShapelyPolygon.from_bounds(*bbox_2d)
                if geom:
                    bbox_srid = 4326
                    if search_request.bbox_crs and self.extension_is_enabled(
                        "CrsExtension"
                    ):
                        bbox_srid = self.get_extension("CrsExtension").epsg_from_crs(
                            search_request.bbox_crs
                        )
                    filter_geom = ga.shape.from_shape(geom, srid=bbox_srid)

                    if bbox_srid == self.storage_srid:
                        query = query.filter(
                            ga.func.ST_Intersects(
                                self.item_table.footprint, filter_geom
                            )
                        )
                    else:
                        query = query.filter(
                            ga.func.ST_Intersects(
                                ga.func.ST_Transform(filter_geom, self.storage_srid),
                                self.item_table.footprint,
                            ),
                        )
                    # Finds and sorts by the input geometry centroid and calculates the distance to the footprint centroid.
                    distance = ga.func.ST_Distance(
                        ga.func.ST_Centroid(
                                ga.func.ST_Envelope(self.item_table.footprint)
                            ),
                            # Footprint in the database are in srid 4326
                            ga.func.ST_Transform(ga.func.ST_GeomFromText(str(geom.centroid),self.storage_srid),self.storage_srid)
                        )
                    query = query.order_by(distance)

                # Temporal query
                if search_request.datetime:
                    # Two tailed query (between)
                    dts = search_request.datetime.split("/")
                    # Non-interval date ex. "2000-02-02T00:00:00.00Z"
                    if len(dts) == 1:
                        query = query.filter(self.item_table.datetime == dts[0])
                    # If both dates are valid strings, it's a between comparison
                    # 2000-02-02T00:00:00.00Z/2000-02-02T00:00:00.00Z
                    elif not any(x in dts for x in ["..", ""]):
                        query = query.filter(self.item_table.datetime.between(*dts))
                    # All items after the start date
                    # 2000-02-02T00:00:00.00Z/.. or 2000-02-02T00:00:00.00Z/
                    elif dts[0] not in ["..", ""]:
                        query = query.filter(self.item_table.datetime >= dts[0])
                    # All items before the end date
                    # ../2000-02-02T00:00:00.00Z or /2000-02-02T00:00:00.00Z
                    elif dts[1] not in ["..", ""]:
                        query = query.filter(self.item_table.datetime <= dts[1])

                if search_request.filter:
                    pygeofilter.backends.sqlalchemy.filters.parse_geometry = monkeypatch_parse_geometry  # monkey patch parse_geometry from pygeofilter
                    sa_expr = to_filter(search_request.filter, self.FIELD_MAPPING)
                    
                    filter_geom = get_geometry_filter(search_request.filter)
                    if filter_geom:
                        # Get the geometry type from filter
                        geom_type = filter_geom.geometry['type']
                        if geom_type  == 'Point' or geom_type == 'Polygon':
                            # Find the center point in the geometry
                            # Need to check if it nested list
                            if geom_type == 'Polygon':
                                if len(filter_geom.geometry['coordinates']) == 1:
                                    client_filter = str(ShapelyPolygon(filter_geom.geometry['coordinates'][0]).centroid)
                                else:
                                    client_filter = str(ShapelyPolygon(filter_geom.geometry['coordinates']).centroid)
                            elif geom_type == 'Point':
                                # Get the coordinates
                                geom_coord = ' '.join(str(f) for f in filter_geom.geometry['coordinates'])

                                client_filter = f"Point ({geom_coord})"

                            # Finds and sorts by the input geometry centroid and calculates the distance to the footprint centroid.
                            distance = ga.func.ST_Distance(
                                ga.func.ST_Centroid(
                                        ga.func.ST_Envelope(self.item_table.footprint)
                                    ),
                                    # Footprint in the database are in srid 4326
                                    ga.func.ST_Transform(ga.func.ST_GeomFromText(client_filter, search_request.filter_crs),4326)
                                )

                            query = query.filter(sa_expr).order_by(distance)
                    else:
                        query = query.filter(sa_expr)
                # Sort
                if search_request.sortby:
                    sort_fields = [
                        getattr(
                            self.item_table.get_field(sort.field),
                            sort.direction.value,
                        )()
                        for sort in search_request.sortby
                    ]
                    sort_fields.append(self.item_table.id)
                    query = query.order_by(*sort_fields)
                else:
                    # Default sort is date
                    query = query.order_by(
                        self.item_table.datetime.desc(), self.item_table.id
                    )

                if self.extension_is_enabled("ContextExtension"):
                    count_query = query.statement.with_only_columns(
                        [func.count()]
                    ).order_by(None)
                    count = query.session.execute(count_query).scalar()

                page = get_page(
                    query, per_page=search_request.limit, page=pagination_token
                )
                # Create dynamic attributes for each page
                page.next = (
                    self.to_token(keyset=page.paging.bookmark_next)
                    if page.paging.has_next
                    else None
                )
                page.previous = (
                    self.to_token(keyset=page.paging.bookmark_previous)
                    if page.paging.has_previous
                    else None
                )

            links = []
            hrefbuilder = self.href_builder(**kwargs)
            if is_direct_post:
                query_params = dict(
                    kwargs["request"]._json
                )  # If direct post, get query_params from json body
            else:
                query_params = dict(kwargs["request"].query_params)
                if "filter" in query_params:
                    query_params["filter"] = json.dumps(
                        json.loads(query_params["filter"])
                    )  # parse and dump json to prettify link in case of "ugly" but valid input formatting

            if not "limit" in query_params:
                query_params.update(
                    {"limit": search_request.limit}
                )  # always include limit

            links.append(
                {
                    "rel": Relations.self.value,
                    "type": "application/geo+json",
                    "href": hrefbuilder.build("./search"),
                    "method": "POST",
                    "body": {
                        **query_params,
                    },
                }
            )
            if search_request.pt:
                links[0]["body"]["pt"] = search_request.pt

            if page.next:
                links.append(
                    {
                        "rel": Relations.next.value,
                        "type": "application/geo+json",
                        "href": hrefbuilder.build("./search"),
                        "method": "POST",
                        "body": {
                            **query_params,
                            "pt": page.next,  # Pagination token must come after query_params for automatic overwrite of "pt"
                        },
                    }
                )
            if page.previous:

                links.append(
                    {
                        "rel": Relations.previous.value,
                        "type": "application/geo+json",
                        "href": hrefbuilder.build("./search"),
                        "method": "POST",
                        "body": {
                            **query_params,
                            "pt": page.previous,
                        },
                    }
                )
            response_features = []
            filter_kwargs = {}

            # rewritten as a list-comprehension to speedup creation of the list
            # Enumerations should be faster than looping and appending
            crs_obj =  {"type": "name",
                "properties": {"name": f"{output_crs}"},
            }
            response_features = [self.item_serializer.db_to_stac(item,hrefbuilder) for i,item in enumerate(page)]

            # Use pydantic includes/excludes syntax to implement fields extension
            if (
                self.extension_is_enabled("FieldsExtension")
                and search_request.field is not None
            ):
                if search_request.filter is not None:
                    query_include: Set[str] = set(
                        [
                            k
                            if k in Settings.get().indexed_fields
                            else f"properties.{k}"
                            for k in search_request.filter_fields
                        ]
                    )
                    if not search_request.field.include:
                        search_request.field.include = query_include
                    else:
                        search_request.field.include.union(query_include)

                filter_kwargs = search_request.field.filter_fields
                # Need to pass through `.json()` for proper serialization
                # of datetime
                response_features = [
                    json.loads(stac_pydantic.Item(**feat).json(**filter_kwargs))
                    for feat,_ in enumerate(response_features)
                ]

        for _,feat in enumerate(response_features):
            feat["crs"] = crs_obj

        context_obj = None
        if self.extension_is_enabled("ContextExtension"):
            context_obj = {
                "returned": len(page),
                "limit": search_request.limit,
                "matched": count,
            }



        return ItemCollection(
            type="FeatureCollection",
            features=response_features,
            links=links,
            context=context_obj,
        )


@attr.s
class CoreFiltersClient(BaseFiltersClient):
    session: Session = attr.ib(default=attr.Factory(Session.create_from_env))

    def validate_collection(self, value):
        # client = CoreCrudClient(session=self.session, collection_table=database.Collection)
        with self.session.session_maker.context_session() as session:
            try:
                CoreCrudClient._lookup_id(value, database.Collection, session)
            except:
                raise ValueError(f"Collection '{value}' doesn't exist")

    def get_queryables(
        self, collection_id: Optional[str] = None, **kwargs
    ) -> Dict[str, Any]:
        """Get the queryables available for the given collection_id.

        If collection_id is None, returns the intersection of all
        queryables over all collections.

        This base implementation returns a blank queryable schema. This is not allowed
        under OGC CQL but it is allowed by the STAC API Filter Extension

        https://github.com/radiantearth/stac-api-spec/tree/master/fragments/filter#queryables
        """

        base_url = str(kwargs["request"].base_url)
        if "id" in kwargs:
            collection_id = kwargs["id"]
            try:
                self.validate_collection(collection_id)
            except ValueError as e:
                raise HTTPException(
                    status_code=404,
                    detail=["Not found"] + str(e).split("\n"),
                )

        # Check that collection exists

        base_queryables, queryables = (
            Queryables.get_queryable_properties_intersection([collection_id])
            if collection_id
            else Queryables.get_queryable_properties_intersection()
        )

        res = {}
        queryables.sort()
        for q in base_queryables + queryables:
            q_type = getattr(QueryableInfo, Queryables.get_queryable(q).name)
            res[q] = {
                "description": q_type[2],
                "$ref" if q_type[3] else "type": q_type[3] if q_type[3] else q_type[1],
            }

        return {
            "$schema": "https://json-schema.org/draft/2019-09/schema",
            "$id": urljoin(
                base_url,
                f"collections/{collection_id}/queryables"
                if collection_id
                else f"queryables",
            ),
            "type": "object",
            "title": f"{collection_id.capitalize() if collection_id else 'Dataforsyningen FlyfotoAPI - Shared queryables'}",
            "properties": res,
        }

def get_geometry_filter(filter):
    """
    Get geometry from filter
    """
    if hasattr(filter, 'geometry'):
        return filter

    lhs, rhs = None, None
    if hasattr(filter, 'lhs'):
        lhs = get_geometry_filter(filter.lhs)
    if hasattr(filter, 'rhs'):
        rhs = get_geometry_filter(filter.rhs)

    if lhs is not None:
        return lhs

    return rhs
