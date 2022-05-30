# encoding: utf-8
"""Filter Extension."""
from enum import Enum
from typing import Callable, List, Type, Union

import attr
from fastapi import APIRouter, FastAPI
from starlette.responses import JSONResponse, Response

from stac_fastapi.api.models import APIRequest, CollectionUri, EmptyRequest
from stac_fastapi.api.routes import create_async_endpoint, create_sync_endpoint
from stac_fastapi.types.core import AsyncBaseFiltersClient, BaseFiltersClient
from stac_fastapi.types.extension import ApiExtension
from stac_fastapi.api import descriptions


class FilterConformanceClasses(str, Enum):
    """Conformance classes for the Filter extension.

    See https://github.com/radiantearth/stac-api-spec/tree/v1.0.0-beta.3/fragments/filter
    """

    # Conformance classes from https://github.com/radiantearth/stac-api-spec/tree/master/fragments/filter
    # CQL-Text, Functions, and Arrays are not supported
    FILTER = "http://www.opengis.net/spec/ogcapi-features-3/1.0/conf/filter"
    ITEM_SEARCH_FILTER = (
        "https://api.stacspec.org/v1.0.0-beta.4/item-search#filter:item-search-filter"
    )
    BASIC_CQL = "http://www.opengis.net/spec/ogcapi-features-3/1.0/conf/basic-cql"
    # CQL_TEXT = "http://www.opengis.net/spec/cql2/1.0/conf/cql2-text"
    CQL_JSON = "http://www.opengis.net/spec/ogcapi-features-3/1.0/conf/cql-json"
    ADVANCED_COMPARISON_OPERATORS = "http://www.opengis.net/spec/ogcapi-features-3/1.0/conf/advanced-comparison-operators"
    BASIC_SPATIAL_OPERATORS = (
        "http://www.opengis.net/spec/ogcapi-features-3/1.0/conf/basic-spatial-operators"
    )
    SPATIAL_OPERATORS = (
        "http://www.opengis.net/spec/ogcapi-features-3/1.0/conf/spatial-operators"
    )
    TEMPORAL_OPERATORS = (
        "http://www.opengis.net/spec/ogcapi-features-3/1.0/conf/temporal-operators"
    )
    # FUNCTIONS = "http://www.opengis.net/spec/ogcapi-features-3/1.0/conf/functions"
    ARITHMETIC = "http://www.opengis.net/spec/ogcapi-features-3/1.0/conf/arithmetic"
    # ARRAYS = "http://www.opengis.net/spec/ogcapi-features-3/1.0/conf/array-operators"
    QUERYABLE_SECOND_OPERAND = (
        "http://www.opengis.net/spec/ogcapi-features-3/1.0/conf/property-property"
    )


@attr.s
class FilterExtension(ApiExtension):
    """Filter Extension.

    The filter extension adds several endpoints which allow the retrieval of queryables and
    provides an expressive mechanism for searching based on Item Attributes:
        GET /queryables
        GET /collections/{collectionId}/queryables

    https://github.com/radiantearth/stac-api-spec/blob/master/fragments/filter/README.md

    Attributes:
        client: Queryables endpoint logic
        conformance_classes: Conformance classes provided by the extension

    """

    client: Union[AsyncBaseFiltersClient, BaseFiltersClient] = attr.ib(
        factory=BaseFiltersClient
    )
    conformance_classes: List[str] = attr.ib(
        default=[
            FilterConformanceClasses.FILTER,
            FilterConformanceClasses.ITEM_SEARCH_FILTER,
            # FilterConformanceClasses.CQL2_TEXT,
            FilterConformanceClasses.CQL_JSON,
            FilterConformanceClasses.BASIC_CQL,
            FilterConformanceClasses.ADVANCED_COMPARISON_OPERATORS,
            FilterConformanceClasses.BASIC_SPATIAL_OPERATORS,
            FilterConformanceClasses.SPATIAL_OPERATORS,
            FilterConformanceClasses.TEMPORAL_OPERATORS,
            # FilterConformanceClasses.FUNCTIONS,
            FilterConformanceClasses.ARITHMETIC,
            # FilterConformanceClasses.ARRAYS,
            FilterConformanceClasses.QUERYABLE_SECOND_OPERAND,
        ]
    )
    router: APIRouter = attr.ib(factory=APIRouter)
    response_class: Type[Response] = attr.ib(default=JSONResponse)

    def _create_endpoint(
        self,
        func: Callable,
        request_type: Union[
            Type[APIRequest],
        ],
    ) -> Callable:
        """Create a FastAPI endpoint."""
        if isinstance(self.client, AsyncBaseFiltersClient):
            return create_async_endpoint(
                func, request_type, response_class=self.response_class
            )
        if isinstance(self.client, BaseFiltersClient):
            return create_sync_endpoint(
                func, request_type, response_class=self.response_class
            )
        raise NotImplementedError

    def register(self, app: FastAPI) -> None:
        """Register the extension with a FastAPI application.

        Args:
            app: target FastAPI application.

        Returns:
            None
        """
        self.router.add_api_route(
            name="Queryables",
            path="/queryables",
            methods=["GET"],
            endpoint=self._create_endpoint(self.client.get_queryables, EmptyRequest),
            description=descriptions.QUERYABLES
        )
        self.router.add_api_route(
            name="Collection Queryables",
            path="/collections/{collectionId}/queryables",
            methods=["GET"],
            endpoint=self._create_endpoint(self.client.get_queryables, CollectionUri),
            description=descriptions.COLLECTION_QUERYABLES
        )

        app.include_router(self.router, tags=["Filter Extension"])
