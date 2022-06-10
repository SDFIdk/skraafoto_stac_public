import operator
import json
import os
import time
import uuid
import pytest
from shapely.geometry import shape
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from random import randint
from urllib.parse import parse_qs, urlparse, urlsplit

import pystac
from pydantic.datetime_parse import parse_datetime
from shapely.geometry import Polygon
from stac_fastapi.types.links import BaseHrefBuilder
from stac_pydantic.shared import DATETIME_RFC339

from stac_fastapi.sqlalchemy.core import CoreCrudClient
from stac_fastapi.types.core import LandingPageMixin


# def test_create_and_delete_item(app_client, load_test_data):
#    """Test creation and deletion of a single item (transactions extension)"""
#    test_item = load_test_data("test_item.json")
#    resp = app_client.post(
#        f"/collections/{test_item['collection']}/items", json=test_item
#    )
#    assert resp.status_code == 200
#
#    resp = app_client.delete(
#        f"/collections/{test_item['collection']}/items/{resp.json()['id']}"
#    )
#    assert resp.status_code == 200


# def test_create_item_conflict(app_client, load_test_data):
#    """Test creation of an item which already exists (transactions extension)"""
#    test_item = load_test_data("test_item.json")
#    resp = app_client.post(
#        f"/collections/{test_item['collection']}/items", json=test_item
#    )
#    assert resp.status_code == 200
#
#    resp = app_client.post(
#        f"/collections/{test_item['collection']}/items", json=test_item
#    )
#    assert resp.status_code == 409


# def test_delete_missing_item(app_client, load_test_data):
#    """Test deletion of an item which does not exist (transactions extension)"""
#    test_item = load_test_data("test_item.json")
#    resp = app_client.delete(f"/collections/{test_item['collection']}/items/hijosh")
#    assert resp.status_code == 404


# def test_create_item_missing_collection(app_client, load_test_data):
#    """Test creation of an item without a parent collection (transactions extension)"""
#    test_item = load_test_data("test_item.json")
#    test_item["collection"] = "stac is cool"
#    resp = app_client.post(
#        f"/collections/{test_item['collection']}/items", json=test_item
#    )
#    assert resp.status_code == 422


# def test_update_item_already_exists(app_client, load_test_data):
#    """Test updating an item which already exists (transactions extension)"""
#    test_item = load_test_data("test_item.json")
#    resp = app_client.post(
#        f"/collections/{test_item['collection']}/items", json=test_item
#    )
#    assert resp.status_code == 200
#
#    assert test_item["properties"]["gsd"] != 16
#    test_item["properties"]["gsd"] = 16
#    resp = app_client.put(
#        f"/collections/{test_item['collection']}/items", json=test_item
#    )
#    updated_item = resp.json()
#    assert updated_item["properties"]["gsd"] == 16


# def test_update_new_item(app_client, load_test_data):
#    """Test updating an item which does not exist (transactions extension)"""
#    test_item = load_test_data("test_item.json")
#    resp = app_client.put(
#        f"/collections/{test_item['collection']}/items", json=test_item
#    )
#    assert resp.status_code == 404


# def test_update_item_missing_collection(app_client, load_test_data):
#    """Test updating an item without a parent collection (transactions extension)"""
#    test_item = load_test_data("test_item.json")
#
#    # Create the item
#    resp = app_client.post(
#        f"/collections/{test_item['collection']}/items", json=test_item
#    )
#    assert resp.status_code == 200
#
#    # Try to update collection of the item
#    test_item["collection"] = "stac is cool"
#    resp = app_client.put(
#        f"/collections/{test_item['collection']}/items", json=test_item
#    )
#    assert resp.status_code == 422


# def test_update_item_geometry(app_client, load_test_data):
#    test_item = load_test_data("test_item.json")
#
#    # Create the item
#    resp = app_client.post(
#        f"/collections/{test_item['collection']}/items", json=test_item
#    )
#    assert resp.status_code == 200
#
#    # Update the geometry of the item
#    test_item["geometry"]["coordinates"] = [[[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]]
#    resp = app_client.put(
#        f"/collections/{test_item['collection']}/items", json=test_item
#    )
#    assert resp.status_code == 200
#
#    # Fetch the updated item
#    resp = app_client.get(
#        f"/collections/{test_item['collection']}/items/{test_item['id']}"
#    )
#    assert resp.status_code == 200
#    assert resp.json()["geometry"]["coordinates"] == [
#        [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
#    ]


def test_get_item(app_client, load_test_data):
    """Test read an item by id (core)"""
    test_item = load_test_data("test_item.json")

    get_item = app_client.get(
        f"/collections/{test_item['collection']}/items/{test_item['id']}"
    )
    assert get_item.status_code == 200
    resp_json = get_item.json()
    assert resp_json["id"] == test_item["id"]


@pytest.mark.skip(
    reason="Validation fails because we allow unknown query parameters due to technical limitations"
)
def test_returns_valid_item(app_client, load_test_data):
    """Test validates fetched item with jsonschema"""
    test_item = load_test_data("test_item.json")

    get_item = app_client.get(
        f"/collections/{test_item['collection']}/items/{test_item['id']}"
    )
    assert get_item.status_code == 200
    item_dict = get_item.json()
    # Mock root to allow validation
    mock_root = pystac.Catalog(
        id="test", description="test desc", href="https://example.com"
    )
    item = pystac.Item.from_dict(item_dict, preserve_dict=False, root=mock_root)
    item.validate()


def test_get_item_collection(app_client, load_test_data):
    """Test read an item collection (core)"""
    test_item = load_test_data("test_item.json")

    resp = app_client.get(f"/collections/{test_item['collection']}/items")
    assert resp.status_code == 200

    item_collection = resp.json()
    assert item_collection["context"]["returned"] == 10


def test_pagination(app_client, load_test_data):
    """Test item collection pagination (paging extension)"""
    item_count = 10
    test_item = load_test_data("test_item.json")

    resp = app_client.get(
        f"/collections/{test_item['collection']}/items", params={"limit": 3}
    )
    assert resp.status_code == 200
    first_page = resp.json()
    assert first_page["context"]["returned"] == 3

    url_components = urlsplit(first_page["links"][0]["href"])
    resp = app_client.get(f"{url_components.path}?{url_components.query}")
    assert resp.status_code == 200
    second_page = resp.json()
    assert second_page["context"]["returned"] == 3


# def test_item_timestamps(app_client, load_test_data):
#    """Test created and updated timestamps (common metadata)"""
#    test_item = load_test_data("test_item.json")
#    start_time = datetime.now(timezone.utc)
#    time.sleep(2)
#    # Confirm `created` timestamp
#    resp = app_client.post(
#        f"/collections/{test_item['collection']}/items", json=test_item
#    )
#    item = resp.json()
#    created_dt = parse_datetime(item["properties"]["created"])
#    assert resp.status_code == 200
#    assert start_time < created_dt < datetime.now(timezone.utc)
#
#    time.sleep(2)
#    # Confirm `updated` timestamp
#    item["properties"]["proj:epsg"] = 4326
#    resp = app_client.put(f"/collections/{test_item['collection']}/items", json=item)
#    assert resp.status_code == 200
#    updated_item = resp.json()
#
#    # Created shouldn't change on update
#    assert item["properties"]["created"] == updated_item["properties"]["created"]
#    assert parse_datetime(updated_item["properties"]["updated"]) > created_dt


def test_item_search_by_id_post(app_client, load_test_data):
    """Test POST search by item id (core)"""
    ids = [
        "2017_82_20_4_2031_00030536",
        "2017_82_19_1_0039_00160059",
        "2017_82_19_2_0039_00160059",
    ]
    test_item = load_test_data("test_item.json")

    params = {"collections": [test_item["collection"]], "ids": ids}
    resp = app_client.post("/search", json=params)
    assert resp.status_code == 200
    resp_json = resp.json()
    assert len(resp_json["features"]) == len(ids)
    assert set([feat["id"] for feat in resp_json["features"]]) == set(ids)


def test_item_search_spatial_query_post(app_client, load_test_data):
    """Test POST search with spatial query (core)"""
    test_item = load_test_data("test_item.json")

    params = {
        "collections": [test_item["collection"]],
        "intersects": test_item["geometry"],
        "limit": 1,
    }
    resp = app_client.post("/search", json=params)
    assert resp.status_code == 200
    resp_json = resp.json()

    # We can't match on just one, because of overlapping geometries
    # assert resp_json["features"][0]["id"] == test_item["id"]
    # Instead just check that we got atleast a hit

    assert len(resp_json["features"]) == 1


def test_item_search_temporal_query_post(app_client, load_test_data):
    """Test POST search with single-tailed spatio-temporal query (core)"""
    test_item = load_test_data("test_item.json")

    item_date = datetime.strptime(test_item["properties"]["datetime"], DATETIME_RFC339)
    item_date = item_date + timedelta(seconds=1)

    params = {
        "collections": [test_item["collection"]],
        "intersects": test_item["geometry"],
        "datetime": f"../{item_date.strftime(DATETIME_RFC339)}",
    }
    resp = app_client.post("/search", json=params)
    resp_json = resp.json()

    assert resp_json["features"][0]["id"] == test_item["id"]


def test_item_search_temporal_window_post(app_client, load_test_data):
    """Test POST search with two-tailed spatio-temporal query (core)"""
    test_item = load_test_data("test_item.json")

    item_date = datetime.strptime(test_item["properties"]["datetime"], DATETIME_RFC339)
    item_date_before = item_date - timedelta(seconds=1)
    item_date_after = item_date + timedelta(seconds=1)

    params = {
        "collections": [test_item["collection"]],
        "intersects": test_item["geometry"],
        "datetime": f"{item_date_before.strftime(DATETIME_RFC339)}/{item_date_after.strftime(DATETIME_RFC339)}",
    }
    resp = app_client.post("/search", json=params)
    resp_json = resp.json()
    assert resp.status_code == 200
    # Query can contain multiple records with same datetime, assert the the test_item is atleast in there.
    assert any(test_item["id"] == f["id"] for f in resp_json["features"])


def test_item_search_temporal_open_window(app_client, load_test_data):
    """Test POST search with open spatio-temporal query (core)"""
    test_item = load_test_data("test_item.json")

    params = {
        "collections": [test_item["collection"]],
        "intersects": test_item["geometry"],
        "datetime": "../..",
    }
    resp = app_client.post("/search", json=params)
    resp_json = resp.json()
    # We can't match on just one, because of overlapping geometries
    # assert resp_json["features"][0]["id"] == test_item["id"]
    # Instead just check that we got atleast a hit
    assert resp.status_code == 200
    assert len(resp_json["features"]) >= 1


def test_item_search_sort_post(app_client, load_test_data):
    """Test POST search with sorting (sort extension)"""
    first_item = load_test_data("test_item.json")
    # Descending
    params = {
        "collections": [first_item["collection"]],
        "sortby": [{"field": "datetime", "direction": "desc"}],
    }
    resp = app_client.post("/search", json=params)
    assert resp.status_code == 200
    resp_json = resp.json()

    assert len(resp_json["features"]) == 10
    date1 = datetime.strptime(
        resp_json["features"][0]["properties"]["datetime"], DATETIME_RFC339
    )
    date10 = datetime.strptime(
        resp_json["features"][9]["properties"]["datetime"], DATETIME_RFC339
    )
    assert date1 > date10
    # Ascending
    params = {
        "collections": [first_item["collection"]],
        "sortby": [{"field": "datetime", "direction": "asc"}],
    }
    resp = app_client.post("/search", json=params)
    assert resp.status_code == 200
    resp_json = resp.json()
    assert len(resp_json["features"]) == 10
    date1 = datetime.strptime(
        resp_json["features"][0]["properties"]["datetime"], DATETIME_RFC339
    )
    date10 = datetime.strptime(
        resp_json["features"][9]["properties"]["datetime"], DATETIME_RFC339
    )
    assert date1 < date10


def test_item_search_by_id_get(app_client, load_test_data):
    """Test GET search by item id (core)"""
    test_item = load_test_data("test_item.json")
    ids = [
        "2017_82_20_4_2031_00030536",
        "2017_82_19_1_0039_00160059",
        "2017_82_19_2_0039_00160059",
    ]

    params = {"collections": test_item["collection"], "ids": ",".join(ids)}
    resp = app_client.get("/search", params=params)
    assert resp.status_code == 200
    resp_json = resp.json()
    assert len(resp_json["features"]) == len(ids)
    assert set([feat["id"] for feat in resp_json["features"]]) == set(ids)


def test_item_search_bbox_get(app_client, load_test_data):
    """Test GET search with spatial query (core)"""
    test_item = load_test_data("test_item.json")
    #resp = app_client.post(
    #    f"/collections/{test_item['collection']}/items", json=test_item
    #)
    #assert resp.status_code == 200

    params = {
        "collections": test_item["collection"],
        "bbox": ",".join([str(coord) for coord in test_item["bbox"]]),
    }
    resp = app_client.get("/search", params=params)
    assert resp.status_code == 200
    resp_json = resp.json()
    assert len(resp_json["features"]) >= 1


def test_item_search_get_without_collections(app_client, load_test_data):
    """Test GET search without specifying collections"""
    test_item = load_test_data("test_item.json")

    params = {
        "bbox": ",".join([str(coord) for coord in test_item["bbox"]]),
    }
    resp = app_client.get("/search", params=params)
    assert resp.status_code == 200
    resp_json = resp.json()
    # Too many hits to determine this
    # assert resp_json["features"][0]["id"] == test_item["id"]
    assert len(resp_json["features"]) >= 1


def test_item_search_temporal_window_get(app_client, load_test_data):
    """Test GET search with spatio-temporal query (core)"""
    test_item = load_test_data("test_item.json")
    #resp = app_client.post(
    #    f"/collections/{test_item['collection']}/items", json=test_item
    #)
    #assert resp.status_code == 200

    item_date = datetime.strptime(test_item["properties"]["datetime"], DATETIME_RFC339)
    item_date_before = item_date - timedelta(seconds=1)
    item_date_after = item_date + timedelta(seconds=1)

    params = {
        "collections": test_item["collection"],
        "datetime": f"{item_date_before.strftime(DATETIME_RFC339)}/{item_date_after.strftime(DATETIME_RFC339)}",
        "limit": 100,
    }
    resp = app_client.get("/search", params=params)
    resp_json = resp.json()

    assert any(
        test_item["id"] == f["id"] for f in resp_json["features"]
    ), "test item should be returned within interval"

    assert all(
        item_date_after
        >= datetime.strptime(f["properties"]["datetime"], DATETIME_RFC339)
        for f in resp_json["features"]
    ), "Item with datetime outside (greater than) filter interval"

    assert all(
        item_date_before
        <= datetime.strptime(f["properties"]["datetime"], DATETIME_RFC339)
        for f in resp_json["features"]
    ), "Item with datetime outside (less than) filter interval"


def test_item_search_temporal_open_interval_get(app_client, load_test_data):
    test_item = load_test_data("test_item.json")

    item_date = datetime.strptime(test_item["properties"]["datetime"], DATETIME_RFC339)

    intervals = [
        (operator.le, f"/{item_date.strftime(DATETIME_RFC339)}"),
        (operator.le, f"../{item_date.strftime(DATETIME_RFC339)}"),
        (operator.ge, f"{item_date.strftime(DATETIME_RFC339)}/"),
        (operator.ge, f"{item_date.strftime(DATETIME_RFC339)}/.."),
    ]
    for ival in intervals:

        params = {
            "collections": test_item["collection"],
            "datetime": ival[1],
            "limit": 100,
        }
        resp = app_client.get("/search", params=params)
        assert resp.status_code == 200

        resp_json = resp.json()
        assert any(
            datetime.strptime(f["properties"]["datetime"], DATETIME_RFC339) != item_date
            for f in resp_json["features"]
        ), f"Expexted more than one distinct datetime in output for interval {ival[1]}"

        comparison_op = ival[0]
        assert all(
            comparison_op(
                datetime.strptime(f["properties"]["datetime"], DATETIME_RFC339),
                item_date,
            )
            for f in resp_json["features"]
        ), f"Item with datetime outside requested interval {ival[1]}"


def test_item_search_sort_get_no_prefix(app_client, load_test_data):
    """Test GET search with sorting with no default prefix(sort extension)"""
    first_item = load_test_data("test_item.json")

    params = {"collections": [first_item["collection"]], "sortby": "datetime"}
    resp = app_client.get("/search", params=params)
    assert resp.status_code == 200


def test_item_search_sort_get(app_client, load_test_data):
    """Test GET search with sorting (sort extension)"""
    first_item = load_test_data("test_item.json")

    params = {"collections": [first_item["collection"]], "sortby": "-datetime"}
    resp = app_client.get("/search", params=params)
    assert resp.status_code == 200
    resp_json = resp.json()
    assert len(resp_json["features"]) == 10
    date1 = datetime.strptime(
        resp_json["features"][0]["properties"]["datetime"], DATETIME_RFC339
    )
    date10 = datetime.strptime(
        resp_json["features"][9]["properties"]["datetime"], DATETIME_RFC339
    )
    assert date1 > date10


def test_item_search_sort_datetime_asc_id_desc_get(app_client, load_test_data):
    """Test GET search with sorting (sort extension)"""
    first_item = load_test_data("test_item.json")

    params = {"collections": [first_item["collection"]], "sortby": "datetime,-id"}
    resp = app_client.get("/search", params=params)

    assert resp.status_code == 200
    resp_json = resp.json()
    assert len(resp_json["features"]) == 10

    id1 = resp_json["features"][0]["id"]
    id10 = resp_json["features"][9]["id"]
    assert id1 > id10

    date1 = datetime.strptime(
        resp_json["features"][0]["properties"]["datetime"], DATETIME_RFC339
    )
    date10 = datetime.strptime(
        resp_json["features"][9]["properties"]["datetime"], DATETIME_RFC339
    )
    assert date1 < date10


def test_item_search_post_without_collection(app_client, load_test_data):
    """Test POST search without specifying a collection"""
    test_item = load_test_data("test_item.json")

    params = {
        "bbox": test_item["bbox"],
    }
    resp = app_client.post("/search", json=params)
    assert resp.status_code == 200
    resp_json = resp.json()
    # Too many hits to determine this
    # assert resp_json["features"][0]["id"] == test_item["id"]
    assert len(resp_json["features"]) >= 1


# We dont have JSONb anymore in the database so this test is obsolete
# def test_item_search_properties_jsonb(app_client, load_test_data):
#    """Test POST search with JSONB query (query extension)"""
#    test_item = load_test_data("test_item.json")
#
#    # EPSG is a JSONB key
#    # params = {"query": {"proj:epsg": {"gt": test_item["properties"]["proj:epsg"] + 1}}}
#    params = {
#        "filter-lang": "cql-json",
#        "filter": {
#            "gt": [{"property": "proj:epsg"}, test_item["properties"]["proj:epsg"] + 1]
#        },
#    }
#    resp = app_client.post("/search", json=params)
#    assert resp.status_code == 200
#    resp_json = resp.json()
#    assert len(resp_json["features"]) == 0


def test_item_search_properties_field(app_client, load_test_data):
    """Test POST search indexed field with query (query extension)"""
    test_item = load_test_data("test_item.json")

    params = {"filter-lang": "cql-json", "filter": {"eq": [{"property": "gsd"}, "-1"]}}
    resp = app_client.post("/search", json=params)
    assert resp.status_code == 200
    resp_json = resp.json()
    assert len(resp_json["features"]) == 0


def test_item_search_get_filter_extension(app_client, load_test_data):
    """Test GET search with JSONB query (filter extension)"""
    test_item = load_test_data("test_item.json")

    params = {
        "collections": [test_item["collection"]],
        "filter-lang": "cql-json",
        "filter": json.dumps(
            {
                "gt": [
                    {"property": "gsd"},
                    test_item["properties"]["gsd"] + 1,
                ]
            }
        ),
    }
    resp = app_client.get("/search", params=params)
    assert resp.json()["context"]["returned"] == 0

    params["filter"] = json.dumps(
        {"eq": [{"property": "gsd"}, test_item["properties"]["gsd"]]}
    )
    resp = app_client.get("/search", params=params)
    resp_json = resp.json()
    assert resp_json["context"]["returned"] >= 2
    assert (
        resp_json["features"][0]["properties"]["gsd"] == test_item["properties"]["gsd"]
    )


def test_get_missing_item_collection(app_client):
    """Test reading a collection which does not exist"""
    resp = app_client.get("/collections/invalid-collection/items")
    assert resp.status_code == 404


# Det lader ikke til at listen af id's bliver ført med ved pagination, kun den sidste kommer med
# TODO: Fix test / eller fix pagination ved liste af id's ( ved ikke helt hvad problemet er)
def test_pagination_item_collection_get(app_client, load_test_data):
    """Test item collection pagination links (paging extension)"""
    test_item = load_test_data("test_item.json")
    ids = [
        "2017_82_20_4_2031_00030536",
        "2017_82_19_1_0039_00160059",
        "2017_82_19_2_0039_00160059",
    ]

    # Paginate through all 3 items with a limit of 1 (expecting 3 requests)
    page = app_client.get(
        f"/collections/{test_item['collection']}/items",
        params={"limit": 1, "ids": ",".join(ids)},
    )
    idx = 0
    item_ids = []
    while True:
        idx += 1
        page_data = page.json()
        item_ids.append(page_data["features"][0]["id"])
        next_link = list(filter(lambda l: l["rel"] == "next", page_data["links"]))
        if not next_link:
            break
        query_params = parse_qs(urlparse(next_link[0]["href"]).query)
        page = app_client.get(
            f"/collections/{test_item['collection']}/items",
            params=query_params,
        )
        # Break here to avoud having an infinite loop in a test case
        if idx > len(ids) + 2:
            break

    # Our limit is 1 so we expect len(ids) number of requests before we run out of pages
    assert idx == len(ids)

    # Confirm we have paginated through all items
    assert not set(item_ids) - set(ids)


# Post virker fint
def test_pagination_post(app_client, load_test_data):
    """Test POST pagination (paging extension)"""
    ids = [
        "2017_82_20_4_2031_00030536",
        "2017_82_19_1_0039_00160059",
        "2017_82_19_2_0039_00160059",
    ]

    # Paginate through all 5 items with a limit of 1 (expecting 5 requests)
    request_body = {"ids": ids, "limit": 1}
    page = app_client.post("/search", json=request_body)
    idx = 0
    item_ids = []
    while True:
        idx += 1
        page_data = page.json()
        item_ids.append(page_data["features"][0]["id"])
        next_link = list(filter(lambda l: l["rel"] == "next", page_data["links"]))
        if not next_link:
            break
        # Merge request bodies
        request_body.update(next_link[0]["body"])
        page = app_client.post("/search", json=request_body)

    # Our limit is 1 so we expect len(ids) number of requests before we run out of pages
    assert idx == len(ids)

    # Confirm we have paginated through all items
    assert not set(item_ids) - set(ids)


# TODO: Page_data kommer ikke tilbage med links her, det er underligt
def test_pagination_token_idempotent(app_client, load_test_data):
    """Test that pagination tokens are idempotent (paging extension)"""
    ids = [
        "2017_82_20_4_2031_00030536",
        "2017_82_19_1_0039_00160059",
        "2017_82_19_2_0039_00160059",
    ]

    page = app_client.get("/search", params={"ids": ",".join(ids), "limit": 1})
    page_data = page.json()
    next_link = list(filter(lambda l: l["rel"] == "next", page_data["links"]))

    assert page_data["links"] != []
    # Confirm token is idempotent
    resp1 = app_client.get(
        "/search", params=parse_qs(urlparse(next_link[0]["href"]).query)
    )
    resp2 = app_client.get(
        "/search", params=parse_qs(urlparse(next_link[0]["href"]).query)
    )
    resp1_data = resp1.json()
    resp2_data = resp2.json()

    # Two different requests with the same pagination token should return the same items
    assert [item["id"] for item in resp1_data["features"]] == [
        item["id"] for item in resp2_data["features"]
    ]


@pytest.mark.skip(reason="FieldExtension switched off")
def test_field_extension_get(app_client, load_test_data):
    """Test GET search with included fields (fields extension)"""

    params = {"fields": "+properties.pers:phi,+properties.gsd"}
    resp = app_client.get("/search", params=params)
    feat_properties = resp.json()["features"][0]["properties"]
    assert not set(feat_properties) - {"pers:phi", "gsd", "datetime"}


@pytest.mark.skip(reason="FieldExtension switched off")
def test_field_extension_post(app_client, load_test_data):
    """Test POST search with included and excluded fields (fields extension)"""

    body = {
        "fields": {
            "exclude": ["datetime"],
            "include": ["properties.pers:phi", "properties.gsd"],
        }
    }

    resp = app_client.post("/search", json=body)
    resp_json = resp.json()
    assert not set(resp_json["features"][0]["properties"]) - {"gsd", "pers:phi"}


@pytest.mark.skip(reason="FieldExtension switched off")
def test_field_extension_exclude_and_include(app_client, load_test_data):
    """Test POST search including/excluding same field (fields extension)"""

    body = {
        "fields": {
            "exclude": ["properties.gsd"],
            "include": ["properties.gsd"],
        }
    }

    resp = app_client.post("/search", json=body)
    resp_json = resp.json()
    assert "properties.gsd" not in resp_json["features"][0]["properties"]


@pytest.mark.skip(reason="FieldExtension switched off")
def test_field_extension_exclude_default_includes(app_client, load_test_data):
    """Test POST search excluding a forbidden field (fields extension)"""

    body = {"fields": {"exclude": ["geometry"]}}

    resp = app_client.post("/search", json=body)
    resp_json = resp.json()
    assert "geometry" not in resp_json["features"][0]


def test_search_intersects_and_bbox(app_client):
    """Test POST search intersects and bbox are mutually exclusive (core)"""
    bbox = [
        6.24,
        52.17,
        13.095,
        58.26,
    ]
    geoj = Polygon.from_bounds(*bbox).__geo_interface__
    params = {"bbox": bbox, "intersects": geoj}
    resp = app_client.post("/search", json=params)
    assert resp.status_code == 400


def test_get_missing_item(app_client, load_test_data):
    """Test read item which does not exist (transactions extension)"""
    test_coll = load_test_data("test_collection.json")
    resp = app_client.get(f"/collections/{test_coll['id']}/items/invalid-item")
    assert resp.status_code == 404


def test_search_invalid_filter_field(app_client):
    body = {
        "filter-lang": "cql-json",
        "filter": {"eq": [{"property": "invalid-field"}, 50]},
    }
    resp = app_client.post("/search", json=body)
    assert resp.status_code == 400


def test_item_search_cql_and(app_client, load_test_data):
    test_item = load_test_data("test_item.json")

    body = {
        "filter-lang": "cql-json",
        "filter": {
            "and": [
                {"eq": [{"property": "gsd"}, test_item["properties"]["gsd"]]},
                {
                    "eq": [
                        {"property": "datetime"},
                        test_item["properties"]["datetime"],
                    ]
                },
            ]
        },
    }
    resp = app_client.post("/search", json=body)
    assert resp.status_code == 200
    resp_json = resp.json()
    assert resp_json["context"]["returned"] >= 1


def test_item_search_cql_or(app_client, load_test_data):
    test_item = load_test_data("test_item.json")

    body = {
        "filter-lang": "cql-json",
        "filter": {
            "or": [
                {"eq": [{"property": "gsd"}, test_item["properties"]["gsd"]]},
                {
                    "eq": [
                        {"property": "datetime"},
                        test_item["properties"]["datetime"] + "1",
                    ]
                },
            ]
        },
    }
    resp = app_client.post("/search", json=body)
    assert resp.status_code == 200
    resp_json = resp.json()
    assert resp_json["context"]["returned"] >= 2


def test_item_search_cql_not(app_client, load_test_data):

    body = {
        "filter-lang": "cql-json",
        "filter": {"not": {"lt": [{"property": "gsd"}, 100]}},
    }
    resp = app_client.post("/search", json=body)
    assert resp.status_code == 200
    resp_json = resp.json()
    assert resp_json["context"]["returned"] == 0


def test_item_search_cql_isNull(app_client, load_test_data):

    body = {"filter-lang": "cql-json", "filter": {"isNull": {"property": "id"}}}
    resp = app_client.post("/search", json=body)
    assert resp.status_code == 200
    resp_json = resp.json()
    assert resp_json["context"]["returned"] == 0


def test_item_search_cql_between(app_client, load_test_data):
    test_item = load_test_data("test_item.json")

    body = {
        "filter-lang": "cql-json",
        "filter": {
            "between": {
                "value": {"property": "gsd"},
                "lower": test_item["properties"]["gsd"] - 1,
                "upper": test_item["properties"]["gsd"] + 1,
            }
        },
    }
    resp = app_client.post("/search", json=body)
    assert resp.status_code == 200
    resp_json = resp.json()
    assert resp_json["context"]["returned"] == 10


def test_item_search_cql_invalid_operation(app_client, load_test_data):
    body = {
        "filter-lang": "cql-json",
        "filter": {"invalid_op": [{"property": "gsd"}, 1]},
    }
    resp = app_client.post("/search", json=body)
    assert resp.status_code == 400


def test_item_search_invalid_filter_lang(app_client, load_test_data):
    body = {
        "filter-lang": "invalid-lang",
        "filter": {"eq": [{"property": "gsd"}, 1]},
    }
    resp = app_client.post("/search", json=body)
    assert resp.status_code == 400


def test_item_search_invalid_filter_crs(app_client, load_test_data):
    body = {
        "filter-crs": "invalid-crs",
        "filter": {"eq": [{"property": "gsd"}, 1]},
    }
    resp = app_client.post("/search", json=body)
    assert resp.status_code == 400


def test_search_bbox_errors(app_client):
    params = {"bbox": "100.0,0.0,0.0,105.0"}
    resp = app_client.get("/search", params=params)
    assert resp.status_code == 400


# def test_filter_crs_bbox_with_crs(app_client, load_test_data):
#     """Test filter with default bbox, result in supported crs (crsExtension)"""
#     test_item = load_test_data("test_item.json")
#     params = {
#         "bbox": ",".join([str(coord) for coord in test_item["bbox"]]),
#         "filter-crs": "http://www.opengis.net/def/crs/EPSG/0/25832",
#         "ids": test_item["id"],
#         "collections": test_item["collection"],
#     }
#     resp = app_client.get("/search", params=params)
#     assert resp.status_code == 200

#     resp_json = resp.json()
#     assert resp_json["features"][0]["id"] == test_item["id"]
#     assert (
#         resp_json["features"][0]["crs"]["properties"]["name"]
#         == "http://www.opengis.net/def/crs/EPSG/0/25832"
#     )


def test_crs_epsg25832(app_client):
    """Test response geometry in crs 25832"""
    params = {"crs": "http://www.opengis.net/def/crs/EPSG/0/25832"}
    resp = app_client.get("/search", params=params)
    resp_json = resp.json()
    assert (
        resp_json["features"][0]["crs"]["properties"]["name"]
        == "http://www.opengis.net/def/crs/EPSG/0/25832"
    )

    body = {"crs": "http://www.opengis.net/def/crs/EPSG/0/25832"}
    resp = app_client.post("/search", json=body)
    resp_json = resp.json()
    assert (
        resp_json["features"][0]["crs"]["properties"]["name"]
        == "http://www.opengis.net/def/crs/EPSG/0/25832"
    )


def test_crs_epsg4326(app_client):
    """Test response geometry in crs 4326"""
    params = {"crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"}
    resp = app_client.get(f"/search", params=params)
    resp_json = resp.json()
    assert (
        resp_json["features"][0]["crs"]["properties"]["name"]
        == "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
    )

    body = {"crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"}
    resp = app_client.post("/search", json=body)
    resp_json = resp.json()
    assert (
        resp_json["features"][0]["crs"]["properties"]["name"]
        == "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
    )


def test_filter_crs_epsg4326(app_client, load_test_data):
    """Test filter with default filter geometry, result in supported crs (crsExtension)"""
    test_item = load_test_data("test_item.json")
    body = {
        "collections": [test_item["collection"]],
        "filter": {"intersects": [{"property": "geometry"}, test_item["geometry"]]},
        "filter-crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84",
        "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84",
        "limit": 200,
    }
    resp = app_client.post("/search", json=body)
    assert resp.status_code == 200

    resp_json = resp.json()
    matching_feat = [x for x in resp_json["features"] if x["id"] == test_item["id"]]
    assert len(matching_feat) == 1
    # Is the geometry "almost" the same. (Which is good enough for this assesment)
    assert shape(matching_feat[0]["geometry"]).almost_equals(shape(test_item["geometry"]))
    assert (
        resp_json["features"][0]["crs"]["properties"]["name"]
        == "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
    )


def test_filter_crs_wrong_filter_crs_epsg25832(app_client, load_test_data):
    """Test filter with default filter geometry, result should return zero items (crsExtension)"""
    test_item = load_test_data("test_item.json")
    body = {
        "collections": [test_item["collection"]],
        "filter": {"intersects": [{"property": "geometry"}, test_item["geometry"]]},
        "filter-crs": "http://www.opengis.net/def/crs/EPSG/0/25832",
        "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84",
        "limit": 200,
    }
    resp = app_client.post("/search", json=body)
    assert resp.status_code == 200

    resp_json = resp.json()
    assert resp.json()["context"]["returned"] == 0
    assert resp.json()["context"]["matched"] == 0


def test_filter_crs_epsg25832(app_client, load_test_data):
    """Test filter with filter geometry in epsg 25832, result in supported crs (crsExtension)"""
    test_item = load_test_data("test_item.json")

    body = {
        "collections": [test_item["collection"]],
        "filter": {
            "intersects": [
                {"property": "geometry"},
                {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [494389.00000000006, 6196260],
                            [493085.00000000006, 6196409.999999999],
                            [493092.99999999994, 6196989.999999999],
                            [494402, 6197140],
                            [494389.00000000006, 6196260],
                        ]
                    ],
                },
            ]
        },
        "filter-crs": "http://www.opengis.net/def/crs/EPSG/0/25832",
        "crs": "http://www.opengis.net/def/crs/EPSG/0/25832",
        "limit": 200,
    }
    resp = app_client.post("/search", json=body)
    assert resp.status_code == 200

    resp_json = resp.json()
    matching_feat = [x for x in resp_json["features"] if x["id"] == test_item["id"]]
    assert len(matching_feat) == 1
    assert (
        resp_json["features"][0]["crs"]["properties"]["name"]
        == "http://www.opengis.net/def/crs/EPSG/0/25832"
    )


def test_filter_get_crs_epsg25832(app_client, load_test_data):
    """Test filter with filter geometry in epsg 25832, result in supported crs (crsExtension)"""
    test_item = load_test_data("test_item.json")

    params = {
        "collections": [test_item["collection"]],
        "filter": json.dumps(
            {
                "intersects": [
                    {"property": "geometry"},
                    {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [494389.00000000006, 6196260],
                                [493085.00000000006, 6196409.999999999],
                                [493092.99999999994, 6196989.999999999],
                                [494402, 6197140],
                                [494389.00000000006, 6196260],
                            ]
                        ],
                    },
                ]
            }
        ),
        "filter-crs": "http://www.opengis.net/def/crs/EPSG/0/25832",
        "crs": "http://www.opengis.net/def/crs/EPSG/0/25832",
        "limit": 200,
    }
    resp = app_client.get("/search", params=params)
    assert resp.status_code == 200, resp.text

    resp_json = resp.json()
    matching_feat = [x for x in resp_json["features"] if x["id"] == test_item["id"]]
    assert len(matching_feat) == 1
    assert (
        resp_json["features"][0]["crs"]["properties"]["name"]
        == "http://www.opengis.net/def/crs/EPSG/0/25832"
    )


def test_single_item_get_bbox_with_bbox_crs(app_client, load_test_data):
    """Test get single item with bbox in supported crs result in default crs (crsExtension)"""
    test_item = load_test_data("test_item.json")
    params = {
        "bbox": ",".join([str(coord) for coord in test_item["bbox"]]),
        "crs": "http://www.opengis.net/def/crs/EPSG/0/25832",
    }
    resp = app_client.get(
        f'/collections/{test_item["collection"]}/items/{test_item["id"]}', params=params
    )
    assert resp.status_code == 200

    resp_json = resp.json()
    # TODO rewrite assertion, but they should not be the same, when i ask in 25832
    assert resp_json["bbox"] != test_item["bbox"]


def test_collection_item_get_bbox_with_bbox_crs(app_client, load_test_data):
    """Test get single item with bbox in supported crs result in default crs (crsExtension)"""
    test_item = load_test_data("test_item.json")
    params = {
        "bbox": ",".join([str(coord) for coord in test_item["bbox"]]),
        "crs": "http://www.opengis.net/def/crs/EPSG/0/25832",
        "limit": 200,
    }
    resp = app_client.get(
        f'/collections/{test_item["collection"]}/items', params=params
    )
    assert resp.status_code == 200

    resp_json = resp.json()

    matching_feat = [x for x in resp_json["features"] if x["id"] == test_item["id"]]
    assert len(matching_feat) == 1
    assert matching_feat[0]["bbox"] != test_item["bbox"]
    assert (
        matching_feat[0]["crs"]["properties"]["name"]
        == "http://www.opengis.net/def/crs/EPSG/0/25832"
    )  # TODO rewrite to uri


def test_single_item_get_bbox_crs_with_crs(app_client, load_test_data):
    """Test get with bbox in supported crs with result in supported crs (crsExtension)"""

    test_item = load_test_data("test_item.json")
    bbox = [492283, 6195600, 493583, 6196470]
    params = {
        "bbox": ",".join([str(coord) for coord in bbox]),
        "bbox-crs": "http://www.opengis.net/def/crs/EPSG/0/25832",
    }
    resp = app_client.get(
        f'/collections/{test_item["collection"]}/items', params=params
    )
    assert resp.status_code == 200

    resp_json = resp.json()
    assert resp_json["context"]["matched"] >= 1


def test_item_search_bbox_crs_with_crs(app_client, load_test_data):
    """Test get with default bbox, result in supported crs(crsExtension)"""
    test_item = load_test_data("test_item.json")
    bbox = [492283, 6195600, 493583, 6196470]
    params = {
        "bbox": ",".join([str(coord) for coord in bbox]),
        "bbox-crs": "http://www.opengis.net/def/crs/EPSG/0/25832",
        "crs": "http://www.opengis.net/def/crs/EPSG/0/25832",
        "limit": 200,
    }
    resp = app_client.get(
        f'/collections/{test_item["collection"]}/items', params=params
    )
    assert resp.status_code == 200

    resp_json = resp.json()

    matching_feat = [x for x in resp_json["features"] if x["id"] == test_item["id"]]
    assert len(matching_feat) == 1
    assert matching_feat[0]["bbox"] != test_item["bbox"]
    assert (
        matching_feat[0]["crs"]["properties"]["name"]
        == "http://www.opengis.net/def/crs/EPSG/0/25832"
    )  # TODO rewrite to uri


def test_item_post_bbox_with_bbox_crs(app_client, load_test_data):
    """Test post with bbox in supported crs result in default crs (crsExtension)"""
    test_item = load_test_data("test_item.json")
    bbox = [492283, 6195600, 493583, 6196470]
    params = {
        "bbox": bbox,
        "ids": [test_item["id"]],
        "collections": [test_item["collection"]],
        "bbox-crs": "http://www.opengis.net/def/crs/EPSG/0/25832",
        # "crs": "http://www.opengis.net/def/crs/EPSG/0/25832",
        "limit": 1,
    }
    resp = app_client.post(f"/search", json=params)
    assert resp.status_code == 200

    resp_json = resp.json()

    matching_feat = [x for x in resp_json["features"] if x["id"] == test_item["id"]]
    assert len(matching_feat) == 1
    assert matching_feat[0]["bbox"] == pytest.approx(test_item["bbox"])
    assert (
        matching_feat[0]["crs"]["properties"]["name"]
        == "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
    )  # TODO rewrite to uri


def test_item_post_bbox_with_crs(app_client, load_test_data):
    """Test post with default bbox, result in supported crs(crsExtension)"""
    test_item = load_test_data("test_item.json")
    bbox = [492283, 6195600, 493583, 6196470]
    params = {
        "bbox": bbox,
        "ids": [test_item["id"]],
        "collections": [test_item["collection"]],
        "bbox-crs": "http://www.opengis.net/def/crs/EPSG/0/25832",
        "crs": "http://www.opengis.net/def/crs/EPSG/0/25832",
        "limit": 1,
    }
    resp = app_client.post(f"/search", json=params)
    assert resp.status_code == 200

    resp_json = resp.json()

    matching_feat = [x for x in resp_json["features"] if x["id"] == test_item["id"]]
    assert len(matching_feat) == 1
    assert matching_feat[0]["bbox"] != test_item["bbox"]
    assert (
        matching_feat[0]["crs"]["properties"]["name"]
        == "http://www.opengis.net/def/crs/EPSG/0/25832"
    )  # TODO rewrite to uri


def test_item_wrong_crs(app_client, load_test_data):
    """Test post with default bbox, response should be an error defining what supported that is crs(crsExtension)"""
    test_item = load_test_data("test_item.json")
    bbox = [492283, 6195600, 493583, 6196470]
    params = {
        "bbox": bbox,
        "ids": [test_item["id"]],
        "collections": [test_item["collection"]],
        "bbox-crs": "http://www.opengis.net/def/crs/EPSG/0/25832",
        "crs": "wrong-crs",
        "limit": 1,
    }
    resp = app_client.post(f"/search", json=params)
    assert resp.status_code == 400

    """Test get with default bbox, response should be an error defining what supported that is crs(crsExtension)"""
    params = {
        "bbox": ",".join([str(coord) for coord in bbox]),
        "bbox-crs": "http://www.opengis.net/def/crs/EPSG/0/25832",
        "crs": "wrong-crs",
        "limit": 1,
    }

    resp = app_client.get(
        f'/collections/{test_item["collection"]}/items', params=params
    )
    assert resp.status_code == 400

    resp = app_client.get(
        f"/collections/{test_item['collection']}/items/{test_item['id']}", params=params
    )
    assert resp.status_code == 400


def test_item_wrong_bbox_crs(app_client, load_test_data):
    """Test post with default bbox, response should be an error defining what supported that is crs(crsExtension)"""
    test_item = load_test_data("test_item.json")
    bbox = [492283, 6195600, 493583, 6196470]
    params = {
        "bbox": bbox,
        "ids": [test_item["id"]],
        "collections": [test_item["collection"]],
        "bbox-crs": "wrong-bbox-crs",
        "crs": "http://www.opengis.net/def/crs/EPSG/0/25832",
        "limit": 1,
    }
    resp = app_client.post(f"/search", json=params)
    assert resp.status_code == 400

    """Test get with default bbox, response should be an error defining what supported that is crs(crsExtension)"""
    params = {
        "bbox": ",".join([str(coord) for coord in bbox]),
        "bbox-crs": "wrong-bbox-crs",
        "crs": "http://www.opengis.net/def/crs/EPSG/0/25832",
        "limit": 1,
    }

    resp = app_client.get(
        f'/collections/{test_item["collection"]}/items', params=params
    )
    assert resp.status_code == 400


def test_conformance_classes_configurable():
    """Test conformance class configurability"""
    landing = LandingPageMixin()
    hrefbuilder = BaseHrefBuilder("http://test/test")
    landing_page = landing._landing_page(
        href_builder=hrefbuilder,
        conformance_classes=["this is a test"],
        extension_schemas=[],
    )
    assert landing_page["conformsTo"][0] == "this is a test"

    # Update environment to avoid key error on client instantiation
    os.environ["CONN_STRING"] = "testing"
    client = CoreCrudClient(base_conformance_classes=["this is a test"])
    assert client.conformance_classes()[0] == "this is a test"
