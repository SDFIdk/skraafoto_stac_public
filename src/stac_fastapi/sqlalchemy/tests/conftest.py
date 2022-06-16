import json
import os
import attr
from typing import Any, Callable, Dict, Type
from fastapi.params import Depends

import pytest
from sqlalchemy.sql.operators import collate
from starlette.testclient import TestClient
import geoalchemy2 as ga
from sqlalchemy.orm import Session as SqlSession, base, with_expression

# from sqlalchemy.orm import Session as with_expression

from stac_fastapi.api.app import StacApi
from stac_fastapi.extensions.core import (
    ContextExtension,
    FieldsExtension,
    QueryExtension,
    SortExtension,
    CrsExtension,
    FilterExtension,
    TransactionExtension,
)
from sqlalchemy.dialects.postgresql import array
from stac_fastapi.sqlalchemy.config import SqlalchemySettings
from stac_fastapi.sqlalchemy.core import CoreCrudClient, CoreFiltersClient
from stac_fastapi.sqlalchemy.models import database
from stac_fastapi.sqlalchemy.session import Session
from stac_fastapi.sqlalchemy.app import (
    token_query_param,
    ROUTES_REQUIRING_TOKEN,
)

from stac_fastapi.sqlalchemy.types.search import STACSearch
from stac_fastapi.types.config import Settings

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TEST_ITEM_ID = "2017_84_41_2_0005_00000519"
TEST_COLLECTION_ID = "skraafotos2017"
BASE_URL = "http://test-server"
from stac_fastapi.sqlalchemy import serializers
from stac_fastapi.sqlalchemy.models import database
from stac_fastapi.sqlalchemy.session import Session
from stac_fastapi.sqlalchemy.types.links import ApiTokenHrefBuilder
from stac_fastapi.types import stac as stac_types
from stac_fastapi.types.core import BaseTransactionsClient
from stac_fastapi.types.errors import NotFoundError


class TestSettings(SqlalchemySettings):
    class Config:
        env_file = ".env.test"


settings = TestSettings()
Settings.set(settings)


@attr.s
class TestTransactionsClient(BaseTransactionsClient):
    """Transactions extension specific CRUD operations."""

    session: Session = attr.ib(default=attr.Factory(Session.create_from_env))
    collection_table: Type[database.Collection] = attr.ib(default=database.Collection)
    item_table: Type[database.ImageView] = attr.ib(default=database.ImageView)
    item_serializer: Type[serializers.Serializer] = attr.ib(
        default=serializers.ItemSerializer
    )
    collection_serializer: Type[serializers.Serializer] = attr.ib(
        default=serializers.CollectionSerializer
    )
    storage_srid: int = attr.ib(default=4326)
    hrefbuilder: ApiTokenHrefBuilder = attr.ib(
        default=ApiTokenHrefBuilder(BASE_URL, token="TOKEN")
    )

    @staticmethod
    def _lookup_id(
        id: str,
        table: Type[database.BaseModel],
        session: Session = attr.ib(default=attr.Factory(Session.create_from_env)),
        query_options: Any = [],
    ) -> Type[database.BaseModel]:
        """Lookup row by id."""
        row = session.query(table).options(query_options).filter(table.id == id).first()
        if not row:
            raise NotFoundError(f"{table.__name__} {id} not found")
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

    def create_item(self, model: stac_types.Item, **kwargs) -> stac_types.Item:
        """Create item."""
        # data = self.item_serializer.stac_to_db(model)
        with self.session.session_maker.context_session() as session:
            # To fake adding an item, fetch an item with an id, copy it and upload it with
            # another id, then return the serialized copy
            options = (
                self._bbox_expression(4326),
                self._geometry_expression(4326),
            )

            item = self._lookup_id(TEST_ITEM_ID, self.item_table, session, options)

            # data["id"] = model["id"]
            # data["collection"] = model["collection"]
            # session.add(data)
            stac_data = self.item_serializer.db_to_stac(item, self.hrefbuilder)
            # Now we do a little cheating instead of creating it, we just fetch it out of the database instead
            stac_data["id"] = model["id"]
            stac_data["collection"] = model["collection"]
            return stac_data

    def create_collection(
        self, model: stac_types.Collection, **kwargs
    ) -> stac_types.Collection:
        """Create collection."""
        data = self.collection_serializer.stac_to_db(model)
        with self.session.session_maker.context_session() as session:
            # session.add(data) # dont actually add anything
            return self.collection_serializer.db_to_stac(data, self.hrefbuilder)

    def update_item(self, model: stac_types.Item, **kwargs) -> stac_types.Item:
        """Update item."""
        with self.session.session_maker.context_session() as session:
            query = session.query(self.item_table).filter(
                self.item_table.id == model["id"]
            )
            if not query.scalar():
                raise NotFoundError(f"Item {model['id']} not found")
            # SQLAlchemy orm updates don't seem to like geoalchemy types
            db_model = self.item_serializer.stac_to_db(model)
            query.update(self.item_serializer.row_to_dict(db_model))
            stac_item = self.item_serializer.db_to_stac(db_model, self.hrefbuilder)

            return stac_item

    def update_collection(
        self, model: stac_types.Collection, **kwargs
    ) -> stac_types.Collection:
        """Update collection."""
        with self.session.session_maker.context_session() as session:
            query = session.query(self.collection_table).filter(
                self.collection_table.id == model["id"]
            )
            if not query.scalar():
                raise NotFoundError(f"Item {model['id']} not found")

            # SQLAlchemy orm updates don't seem to like geoalchemy types
            db_model = self.collection_serializer.stac_to_db(model)
            # query.update(self.collection_serializer.row_to_dict(db_model))

            return self.collection_serializer.db_to_stac(db_model, self.hrefbuilder)

    def delete_item(
        self, item_id: str, collection_id: str, **kwargs
    ) -> stac_types.Item:
        """Delete item."""
        with self.session.session_maker.context_session() as session:
            query = session.query(self.item_table).filter(self.item_table.id == item_id)
            data = query.first()
            if not data:
                raise NotFoundError(f"Item {item_id} not found")
            # query.delete() # Dont actually delete anything
            return self.item_serializer.db_to_stac(data, self.hrefbuilder)

    def delete_collection(self, id: str, **kwargs) -> stac_types.Collection:
        """Delete collection."""
        with self.session.session_maker.context_session() as session:
            query = session.query(self.collection_table).filter(
                self.collection_table.id == id
            )
            data = query.first()
            if not data:
                raise NotFoundError(f"Collection {id} not found")
            # query.delete() # dont actually delete anything
            return self.collection_serializer.db_to_stac(data, self.hrefbuilder)


@pytest.fixture(autouse=True)
def cleanup(
    postgres_core: CoreCrudClient, postgres_transactions: TestTransactionsClient
):
    yield
    collections = postgres_core.all_collections(request=MockStarletteRequest)
    for coll in collections["collections"]:
        if coll["id"].split("-")[0] == "test":
            # Delete the items
            items = postgres_core.item_collection(
                coll["id"], limit=100, request=MockStarletteRequest
            )
            for feat in items["features"]:
                postgres_transactions.delete_item(
                    feat["id"], feat["collection"], request=MockStarletteRequest
                )

            # Delete the collection
            postgres_transactions.delete_collection(
                coll["id"], request=MockStarletteRequest
            )


@pytest.fixture
def load_test_data() -> Callable[[str], Dict]:
    def load_file(filename: str) -> Dict:
        with open(os.path.join(DATA_DIR, filename)) as file:
            return json.load(file)

    return load_file


@pytest.fixture
def test_data_id() -> str:
    return "test-collection"


class MockStarletteRequest:
    base_url = BASE_URL
    query_params = {}


@pytest.fixture
def db_session() -> Session:

    settings = SqlalchemySettings()
    session = Session.create_from_settings(settings)
    return session


@pytest.fixture
def postgres_core(db_session):
    return CoreCrudClient(
        session=db_session,
        item_table=database.ImageView,
        collection_table=database.Collection,
        storage_srid=4326,
    )


@pytest.fixture
def postgres_transactions(db_session):
    return TestTransactionsClient(
        session=db_session,
        item_table=database.ImageView,
        collection_table=database.Collection,
        storage_srid=4326,
    )


@pytest.fixture
def api_client(db_session):
    settings = SqlalchemySettings()
    return StacApi(
        settings=settings,
        client=CoreCrudClient(session=db_session, storage_srid=4326),
        extensions=[
            CrsExtension(),
            ContextExtension(),
            SortExtension(),
            # FieldsExtension(),
            # QueryExtension(),
            TransactionExtension(
                client=TestTransactionsClient(session=db_session, storage_srid=25832),
                settings=settings,
            ),
            FilterExtension(client=CoreFiltersClient(session=db_session)),
        ],
        search_request_model=STACSearch,
    )


@pytest.fixture
def app_client(api_client, load_test_data, postgres_transactions):
    # coll = load_test_data("test_collection.json")
    # postgres_transactions.create_collection(coll, request=MockStarletteRequest)

    with TestClient(api_client.app) as test_app:
        yield test_app


@pytest.fixture
def token_app_client(api_client):
    """Gets a TestClient with an app that requires `token` for some paths"""
    api_client.add_route_dependencies(
        scopes=ROUTES_REQUIRING_TOKEN,
        dependencies=[Depends(token_query_param)],
    )
    with TestClient(api_client.app) as test_app:
        yield test_app
