"""FastAPI application."""
import logging
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


def token_query_param(
    token: str = Depends(security.api_key.APIKeyQuery(name="token", auto_error=False)),
):
    """This defines an api-key query param named 'token'"""
    # Set auto_error to `True` to make `token `required.
    pass


# Here we add all paths which produces internal links as they must include the token
ROUTES_REQUIRING_TOKEN = [
    {"path": "/", "method": "GET"},
    {"path": "/search", "method": "GET"},
    {"path": "/search", "method": "POST"},
    {"path": "/collections", "method": "GET"},
    {"path": "/collections/{collectionId}", "method": "GET"},
    {"path": "/collections/{collectionId}/items", "method": "GET"},
    {"path": "/collections/{collectionId}/items/{itemId}", "method": "GET"},
]

settings = SqlalchemySettings()

if settings.debug:
    logging.basicConfig(level="DEBUG")
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

session = Session.create_from_settings(settings)
api = StacApi(
    title="Dataforsyningen FlyfotoAPI",
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
    route_dependencies=[(ROUTES_REQUIRING_TOKEN, [Depends(token_query_param)])],
)
app = api.app

# Set 'host', 'root_path' and 'protocol' from x-forwarded-xxx headers
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts=settings.trusted_hosts)


if settings.debug:
    from fastapi import Request

    # Log request headers to be able to debug proxying issue #8
    @app.middleware("http")
    async def log_request_headers(request: Request, call_next):
        logging.debug(request.headers)
        response = await call_next(request)
        return response


# def run():
#     """Run app from command line using uvicorn if available."""
#     try:
#         import uvicorn

#         uvicorn.run(
#             "stac_fastapi.sqlalchemy.app:app",
#             host=settings.app_host,
#             port=settings.app_port,
#             log_level="info",
#             reload=settings.reload,
#         )
#     except ImportError:
#         raise RuntimeError("Uvicorn must be installed in order to use command")


# if __name__ == "__main__":
#     run()


# def create_handler(app):
#     """Create a handler to use with AWS Lambda if mangum available."""
#     try:
#         # from mangum import Mangum

#         # return Mangum(app)
#         pass
#     except ImportError:
#         return None


# handler = create_handler(app)
