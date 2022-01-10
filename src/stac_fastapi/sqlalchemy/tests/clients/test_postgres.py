import uuid
from copy import deepcopy
from typing import Callable

import pytest
from stac_pydantic import Collection, Item
from tests.conftest import MockStarletteRequest
from stac_fastapi.types import stac as stac_types
from stac_fastapi.api.app import StacApi
from stac_fastapi.sqlalchemy.core import CoreCrudClient

from stac_fastapi.types.errors import ConflictError, NotFoundError
from ..conftest import TestTransactionsClient


def test_get_collection(
    postgres_core: CoreCrudClient,
    postgres_transactions: TestTransactionsClient,
    load_test_data: Callable,
):
    data = load_test_data("test_collection.json")
    postgres_transactions.create_collection(data, request=MockStarletteRequest)
    coll = postgres_core.get_collection(data["id"], request=MockStarletteRequest)
    # assert Collection(**data).dict(exclude={"links"}) == Collection(**coll).dict(
    #    exclude={"links"}
    # )
    assert coll["id"] == data["id"]


def test_get_collection_items(
    postgres_core: CoreCrudClient,
    load_test_data: Callable,
):
    coll = load_test_data("test_collection.json")
    fc = postgres_core.item_collection(coll["id"], request=MockStarletteRequest)

    assert len(fc["features"]) == 10
    for item in fc["features"]:
        assert item["collection"] == coll["id"]


# def test_create_item(
#    postgres_core: CoreCrudClient,
#    postgres_transactions: TestTransactionsClient,
#    load_test_data: Callable,
# ):
#    coll = load_test_data("test_collection.json")
#    postgres_transactions.create_collection(coll, request=MockStarletteRequest)
#    item = load_test_data("test_item.json")
#    postgres_transactions.create_item(item, request=MockStarletteRequest)
#    resp = postgres_core.get_item(
#        item["id"], item["collection"], request=MockStarletteRequest
#    )
#    assert Item(**item).dict(
#        exclude={"links": ..., "properties": {"created", "updated"}}
#    ) == Item(**resp).dict(exclude={"links": ..., "properties": {"created", "updated"}})


# def test_create_item_already_exists(
#    postgres_transactions: TestTransactionsClient,
#    load_test_data: Callable,
# ):
#    coll = load_test_data("test_collection.json")
#    postgres_transactions.create_collection(coll, request=MockStarletteRequest)
#    item = load_test_data("test_item.json")
#    postgres_transactions.create_item(item, request=MockStarletteRequest)
#    with pytest.raises(ConflictError):
#        postgres_transactions.create_item(item, request=MockStarletteRequest)


# def test_update_item(
#    postgres_core: CoreCrudClient,
#    postgres_transactions: TestTransactionsClient,
#    load_test_data: Callable,
# ):
#    coll = load_test_data("test_collection.json")
#    postgres_transactions.create_collection(coll, request=MockStarletteRequest)
#    item = load_test_data("test_item.json")
#    postgres_transactions.create_item(item, request=MockStarletteRequest)
#    item["properties"]["foo"] = "bar"
#    postgres_transactions.update_item(item, request=MockStarletteRequest)
#    updated_item = postgres_core.get_item(
#        item["id"], item["collection"], request=MockStarletteRequest
#    )
#    assert updated_item["properties"]["foo"] == "bar"


# def test_update_geometry(
#    postgres_core: CoreCrudClient,
#    postgres_transactions: TestTransactionsClient,
#    load_test_data: Callable,
# ):
#    coll = load_test_data("test_collection.json")
#    postgres_transactions.create_collection(coll, request=MockStarletteRequest)
#    item = load_test_data("test_item.json")
#    postgres_transactions.create_item(item, request=MockStarletteRequest)
#    item["geometry"]["coordinates"] = [[[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]]
#    postgres_transactions.update_item(item, request=MockStarletteRequest)
#    updated_item = postgres_core.get_item(
#        item["id"], item["collection"], request=MockStarletteRequest
#    )
#    assert updated_item["geometry"]["coordinates"] == item["geometry"]["coordinates"]


# def test_delete_item(
#    postgres_core: CoreCrudClient,
#    postgres_transactions: TestTransactionsClient,
#    load_test_data: Callable,
# ):
#    coll = load_test_data("test_collection.json")
#    postgres_transactions.create_collection(coll, request=MockStarletteRequest)
#    item = load_test_data("test_item.json")
#    postgres_transactions.create_item(item, request=MockStarletteRequest)
#    postgres_transactions.delete_item(
#        item["id"], item["collection"], request=MockStarletteRequest
#    )
#    with pytest.raises(NotFoundError):
#        postgres_core.get_item(
#            item["id"], item["collection"], request=MockStarletteRequest
#        )
#


def test_landing_page_no_collection_title(
    postgres_core: CoreCrudClient,
    postgres_transactions: TestTransactionsClient,
    load_test_data: Callable,
    api_client: StacApi,
):
    class MockStarletteRequestWithApp(MockStarletteRequest):
        app = api_client.app

    coll = load_test_data("test_collection.json")
    del coll["title"]
    postgres_transactions.create_collection(coll, request=MockStarletteRequest)
    landing_page = postgres_core.landing_page(request=MockStarletteRequestWithApp)
    for link in landing_page["links"]:
        if link["href"].split("/")[-1] == coll["id"]:
            assert link["title"]
