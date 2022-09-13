"""FastAPI application."""
import logging
from typing import Optional
from fastapi import security
from fastapi.params import Depends, Query
from stac_fastapi.api.app import StacApi
from stac_fastapi.extensions.core import (
    FieldsExtension,
    FilterExtension,
    CrsExtension,
    SortExtension,
    ContextExtension,
)
from stac_fastapi.sqlalchemy.config import SqlalchemySettings
from stac_fastapi.sqlalchemy.models import database
from stac_fastapi.sqlalchemy.core import CoreCrudClient, CoreFiltersClient
from stac_fastapi.sqlalchemy.session import Session
from stac_fastapi.sqlalchemy.types.search import STACSearch
from stac_fastapi.sqlalchemy.middlewares.proxy_headers import ProxyHeadersMiddleware
from sqlalchemy import event
from sqlalchemy.engine import Engine
import time
import logging

def token_header_param(
    header_token: Optional[str] = Depends(
        security.api_key.APIKeyHeader(name="token", auto_error=False)
    ),
):
    """This defines an api-key header param named 'token'"""
    # Set auto_error to `True` to make `token `required.
    pass


def token_query_param(
    query_token: Optional[str] = Depends(
        security.api_key.APIKeyQuery(name="token", auto_error=False)
    ),
):
    """This defines an api-key query param named 'token'"""
    # Set auto_error to `True` to make `token `required.
    pass


# Here we add all paths which produces internal links as they must include the token
ROUTES_REQUIRING_TOKEN = [
    {"path": "/", "method": "GET"},
    {"path": "/conformance", "method": "GET"},
    {"path": "/search", "method": "GET"},
    {"path": "/search", "method": "POST"},
    {"path": "/collections", "method": "GET"},
    {"path": "/collections/{collectionId}", "method": "GET"},
    {"path": "/collections/{collectionId}/items", "method": "GET"},
    {"path": "/collections/{collectionId}/items/{itemId}", "method": "GET"},
    {"path": "/queryables", "method": "GET"},
    {"path": "/collections/{collectionId}/queryables", "method": "GET"},
    {"path": "/_mgmt/ping", "method": "GET"},
]

settings = SqlalchemySettings(connect_args={
    "options": "-c statement_timeout=10000"
})

if settings.debug:
    logging.basicConfig(level="DEBUG",
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    @event.listens_for(Engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement,
                            parameters, context, executemany):
        conn.info.setdefault('query_start_time', []).append(time.time())
        logging.debug("Start Query: %s", statement)

    @event.listens_for(Engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement,
                            parameters, context, executemany):
        total = time.time() - conn.info['query_start_time'].pop(-1)
        logging.debug("Query Complete!")
        logging.debug("Total Time: %f", total)
        
session = Session.create_from_settings(settings)
api = StacApi(
    title="Skråfoto STAC API",
    description="API til udstilling af metadata for ikke-oprettede flyfotos.",
    settings=settings,
    extensions=[
        # FieldsExtension(),
        FilterExtension(client=CoreFiltersClient(session=session)),
        SortExtension(),
        ContextExtension(),
        CrsExtension(),
    ],
    client=CoreCrudClient(
        session=session,
        collection_table=database.Collection,
        landing_page_id="dataforsyningen-flyfotoapi",
    ),
    search_request_model=STACSearch,
    route_dependencies=[(ROUTES_REQUIRING_TOKEN, [Depends(token_header_param), Depends(token_query_param)])],
)
app = api.app

# Set 'host', 'root_path' and 'protocol' from x-forwarded-xxx headers
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts=settings.trusted_hosts)

#if settings.debug:
#    add_timing_middleware(app, record=logging.debug, prefix="app", exclude="untimed")

if settings.debug:
    from fastapi import Request

    # Log request headers to be able to debug proxying issue #8
    @app.middleware("http")
    async def log_request_headers(request: Request, call_next):
        logging.debug(request.headers)
        response = await call_next(request)
        return response
