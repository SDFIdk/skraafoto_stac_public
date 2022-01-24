"""Serializers."""
import abc
import json
from datetime import datetime, timedelta, timezone
from typing import Dict, TypedDict, Any
import urllib.parse

import attr
import geoalchemy2 as ga
from stac_pydantic.shared import DATETIME_RFC339

from stac_fastapi.sqlalchemy.models import database
from stac_fastapi.sqlalchemy.types.links import ApiTokenHrefBuilder
from stac_fastapi.sqlalchemy.config import SqlalchemySettings
from stac_fastapi.types import stac as stac_types

from stac_fastapi.types.links import (
    CollectionLinks,
    ItemLinks,
    resolve_links,
)

DATE_RFC339 = "%Y-%m-%d"
UTC_TIMEZONE = timezone(timedelta(0))
settings = SqlalchemySettings()


def _add_query_params(url, params):
    if not params:
        return url
    url_parts = list(urllib.parse.urlparse(url))
    query = dict(urllib.parse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urllib.parse.urlencode(query)
    return urllib.parse.urlunparse(url_parts)


@attr.s  # type:ignore
class Serializer(abc.ABC):
    """Defines serialization methods between the API and the data model."""

    @classmethod
    @abc.abstractmethod
    def db_to_stac(
        cls, db_model: database.BaseModel, hrefbuilder: ApiTokenHrefBuilder
    ) -> TypedDict:
        """Transform database model to stac."""
        ...

    @classmethod
    @abc.abstractmethod
    def stac_to_db(
        cls, stac_data: TypedDict, exclude_geometry: bool = False
    ) -> database.BaseModel:
        """Transform stac to database model."""
        ...

    @classmethod
    def row_to_dict(cls, db_model: database.BaseModel):
        """Transform a database model to it's dictionary representation."""
        d = {}
        for column in db_model.__table__.columns:
            value = getattr(db_model, column.name)
            if value:
                d[column.name] = value
        return d


class ItemSerializer(Serializer):
    """Serialization methods for STAC items."""

    @classmethod
    def _add_if_not_none(cls, dict: Dict, key: str, val: Any):
        """Adds value to dictionary with specified key if value is not None"""
        if val is not None:
            dict[key] = val

    @classmethod
    def db_to_stac(
        cls, db_model: database.ImageView, hrefbuilder: ApiTokenHrefBuilder
    ) -> stac_types.Item:
        """Transform database model to stac item."""
        properties = db_model.properties.copy()
        indexed_fields = settings.indexed_fields
        for field in indexed_fields:
            # Use getattr to accommodate extension namespaces
            field_value = getattr(db_model, field.split(":")[-1])
            if field == "datetime":
                # Postgres returns datetime in client time zone. Convert to UTC and format as string with Z
                field_value = field_value.astimezone(timezone(timedelta(0))).strftime(
                    DATETIME_RFC339
                )
            properties[field] = field_value
        item_id = db_model.id
        collection_id = db_model.collection_id
        item_links = ItemLinks(
            collection_id=collection_id, item_id=item_id, href_builder=hrefbuilder
        ).create_links()

        token_param = {"token": hrefbuilder.token} if hrefbuilder.token else {}
        cog_url = _add_query_params(
            f"{settings.cog_file_server_basepath}/{db_model.data_path}", token_param
        )
        encoded_cog_url = urllib.parse.quote(cog_url, safe="")
        tiler_params = {"url": encoded_cog_url, **token_param}

        add_links = [
            {
                "rel": "license",
                "href": "https://sdfe.dk/om-os/vilkaar-og-priser",
                "type": "text/html; charset=UTF-8",
                "title": "SDFE license terms",
            },
            {
                "rel": "alternate",
                "href": _add_query_params(
                    f"{settings.cogtiler_basepath}/viewer.html", tiler_params
                ),
                "type": "text/html; charset=UTF-8",
                "title": "Interactive image viewer",
            },
        ]
        item_links += add_links

        stac_extensions = [
            "https://stac-extensions.github.io/view/v1.0.0/schema.json",
            "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
            "https://raw.githubusercontent.com/stac-extensions/perspective-imagery/main/json-schema/schema.json",  # TODO: Change when published...
        ]

        assets = {
            "data": {
                "href": cog_url,
                "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                "roles": ["data"],
                "title": "Raw tiff file",
            },
            "thumbnail": {
                "href": _add_query_params(
                    f"{settings.cogtiler_basepath}/thumbnail.jpg", tiler_params
                ),
                "type": "image/jpeg",
                "roles": ["thumbnail"],
                "title": "Thumbnail",
            },
        }

        # The custom geometry we are using emits geojson if the geometry is bound to the database
        # Otherwise it will return a geoalchemy2 WKBElement
        # TODO: It's probably best to just remove the custom geometry type
        geometry = db_model.footprint
        if isinstance(geometry, ga.elements.WKBElement):
            geometry = ga.shape.to_shape(geometry).__geo_interface__
        if isinstance(geometry, str):
            geometry = json.loads(geometry)

        # Properties TODO: break into seperate method

        # General props
        instrument_id = db_model.camera_id  # Used here and for pers:cam_id
        cls._add_if_not_none(properties, "gsd", db_model.gsd)
        properties["license"] = "various"
        cls._add_if_not_none(properties, "platform", "Fixed-wing aircraft")
        cls._add_if_not_none(properties, "instruments", [instrument_id])
        properties["providers"] = [
            {"name": db_model.producer, "roles": ["producer", "processor"]},
            {"url": "https://sdfe.dk/", "name": "SDFE", "roles": ["licensor", "host"]},
        ]

        # Proj: https://github.com/stac-extensions/projection
        properties["proj:epsg"] = None
        # TODO: sensor_area_xxx seems to be a mix between pixels and mm
        properties["proj:shape"] = [
            db_model.sensor_rows,
            db_model.sensor_columns,
        ]  # Number of pixels in Y and X directions

        # View: https://github.com/stac-extensions/view
        cls._add_if_not_none(properties, "view:azimuth", db_model.azimuth)
        cls._add_if_not_none(properties, "view:off_nadir", db_model.offnadir)

        # Homegrown sdfe
        properties["direction"] = db_model.direction
        properties["estimated_accuracy"] = db_model.estacc

        # Perspective
        properties["pers:omega"] = db_model.omega
        properties["pers:phi"] = db_model.phi
        properties["pers:kappa"] = db_model.kappa
        properties["pers:perspective_center"] = [
            db_model.easting,
            db_model.northing,
            db_model.height,
        ]
        properties["pers:crs"] = db_model.horisontal_crs
        properties["pers:vertical_crs"] = db_model.vertical_crs
        properties["pers:rotation_matrix"] = db_model.rotmatrix

        properties["pers:interior_orientation"] = {
            "camera_id": instrument_id,
            "focal_length": db_model.focal_length,
            "pixel_spacing": [db_model.sensor_pixel_size, db_model.sensor_pixel_size],
            "calibration_date": db_model.calibration_date.strftime(DATE_RFC339)
            if db_model.calibration_date
            else None,
            "principal_point_offset": [
                db_model.principal_point_x,
                db_model.principal_point_y,
            ],  # Principal point offset in mm as [offset_x, offset_y]
            "sensor_array_dimensions": [
                db_model.sensor_rows,
                db_model.sensor_columns,
            ],  # Sensor dimensions as [number_of_columns, number_of_rows]
        }

        # Simple OGC API Features clients do not support "assets". Copy most important to the properties collection
        for copy_asset in ["data", "thumbnail"]:
            properties[f"asset:{copy_asset}"] = assets[copy_asset]["href"]

        return stac_types.Item(
            type="Feature",
            stac_version="1.0.0",
            stac_extensions=stac_extensions,
            id=db_model.id,
            collection=db_model.collection_id,
            geometry=geometry,
            bbox=[float(x) for x in db_model.bbox],
            properties=properties,
            links=item_links,
            assets=assets,
        )


class CollectionSerializer(Serializer):
    """Serialization methods for STAC collections."""

    @classmethod
    def db_to_stac(
        cls, db_model: database.Collection, hrefbuilder: ApiTokenHrefBuilder
    ) -> TypedDict:
        """Transform database model to stac collection."""
        collection_links = CollectionLinks(
            collection_id=db_model.id, href_builder=hrefbuilder
        ).create_links()

        db_links = db_model.links
        if db_links:
            collection_links += resolve_links(db_links, hrefbuilder.base_url)

        stac_extensions = db_model.stac_extensions or []
        try:
            if isinstance(db_model, database.CrsCollection):
                return stac_types.Collection(
                    type="Collection",
                    id=db_model.id,
                    stac_extensions=stac_extensions,
                    stac_version=db_model.stac_version,
                    title=db_model.title,
                    description=db_model.description,
                    keywords=db_model.keywords,
                    storageCrs=db_model.storageCrs,
                    crs=[],  # Gets update after serialization by the crs extension
                    license=db_model.license,
                    providers=db_model.providers,
                    summaries=db_model.summaries,
                    extent=db_model.extent,
                    links=collection_links,
                )
        except:
            pass  # TODO: raise some error

        return stac_types.Collection(
            type="Collection",
            id=db_model.id,
            stac_extensions=stac_extensions,
            stac_version=db_model.stac_version,
            title=db_model.title,
            description=db_model.description,
            keywords=db_model.keywords,
            license=db_model.license,
            providers=db_model.providers,
            summaries=db_model.summaries,
            extent=db_model.extent,
            links=collection_links,
        )

    @classmethod
    def stac_to_db(
        cls, stac_data: TypedDict, exclude_geometry: bool = False
    ) -> database.Collection:
        """Transform stac collection to database model."""
        if "crs" in stac_data:
            del stac_data["crs"]
        return database.Collection(**dict(stac_data))
