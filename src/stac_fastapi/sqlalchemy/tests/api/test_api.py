from datetime import datetime, timedelta
import json
from ..conftest import TEST_COLLECTION_ID, MockStarletteRequest
from stac_fastapi.sqlalchemy.config import (
    SkraafotosProperties,
    BaseQueryables,
    QueryableInfo,
)

STAC_CORE_ROUTES = [
    "GET /",
    "GET /collections",
    "GET /collections/{collectionId}",
    "GET /collections/{collectionId}/items",
    "GET /collections/{collectionId}/items/{itemId}",
    "GET /conformance",
    "GET /search",
    "POST /search",
]
STAC_ROUTES_REQUIRING_TOKEN = [
    {"path": "/", "method": "GET"},
    {"path": "/search", "method": "GET"},
    {"path": "/search", "method": "POST"},
    {"path": "/collections", "method": "GET"},
    {"path": "/collections/{collectionId}", "method": "GET"},
    {"path": "/collections/{collectionId}/items", "method": "GET"},
    {"path": "/collections/{collectionId}/items/{itemId}", "method": "GET"},
]
TEST_COLLECTION_ID = "skraafotos2017"


def test_core_router(api_client):
    core_routes = set(STAC_CORE_ROUTES)
    api_routes = set(
        [f"{list(route.methods)[0]} {route.path}" for route in api_client.app.routes]
    )
    assert not core_routes - api_routes


def test_app_search_response(load_test_data, app_client, postgres_transactions):
    item = load_test_data("test_item.json")
    postgres_transactions.create_item(item, request=MockStarletteRequest)

    resp = app_client.get("/search", params={"collections": [TEST_COLLECTION_ID]})
    assert resp.status_code == 200
    resp_json = resp.json()

    assert resp_json.get("type") == "FeatureCollection"
    # stac_version and stac_extensions were removed in v1.0.0-beta.3
    assert resp_json.get("stac_version") is None
    assert resp_json.get("stac_extensions") is None


def test_app_context_extension(load_test_data, app_client, postgres_transactions):
    item = load_test_data("test_item.json")
    postgres_transactions.create_item(item, request=MockStarletteRequest)

    resp = app_client.get("/search", params={"collections": [TEST_COLLECTION_ID]})
    assert resp.status_code == 200
    resp_json = resp.json()
    assert "context" in resp_json
    if resp_json["context"]["returned"] == resp_json["context"]["limit"]:
        assert resp_json["context"]["limit"] < resp_json["context"]["matched"]
    else:
        assert resp_json["context"]["limit"] > resp_json["context"]["matched"]


def test_app_fields_extension(load_test_data, app_client, postgres_transactions):
    item = load_test_data("test_item.json")
    postgres_transactions.create_item(item, request=MockStarletteRequest)

    resp = app_client.get(
        "/search", params={"collections": [TEST_COLLECTION_ID], "fields": ""}
    )
    assert resp.status_code == 200
    resp_json = resp.json()
    assert list(resp_json["features"][0]["properties"]) == ["datetime"]


def test_app_filter_extension_gt(load_test_data, app_client, postgres_transactions):
    test_item = load_test_data("test_item.json")
    postgres_transactions.create_item(test_item, request=MockStarletteRequest)
    params = {
        "filter-lang": "cql-json",
        "filter": {
            "gt": [{"property": "pers:phi"}, test_item["properties"]["pers:phi"]]
        },
    }
    resp = app_client.post("/search", json=params)
    assert resp.status_code == 200
    resp_json = resp.json()
    assert len(resp_json["features"]) > 0


def test_app_filter_extension_gte(load_test_data, app_client, postgres_transactions):
    test_item = load_test_data("test_item.json")
    postgres_transactions.create_item(test_item, request=MockStarletteRequest)
    params = {
        "filter-lang": "cql-json",
        "filter": {
            "gte": [{"property": "pers:phi"}, test_item["properties"]["pers:phi"]]
        },
    }
    resp = app_client.post("/search", json=params)
    assert resp.status_code == 200
    resp_json = resp.json()
    assert len(resp_json["features"]) > 0


def test_app_filter_extension_limit_lt0(
    load_test_data, app_client, postgres_transactions
):
    item = load_test_data("test_item.json")
    postgres_transactions.create_item(item, request=MockStarletteRequest)

    params = {"limit": -1}
    resp = app_client.post("/search", json=params)
    assert resp.status_code == 400


def test_app_filter_extension_limit_gt10000(
    load_test_data, app_client, postgres_transactions
):
    item = load_test_data("test_item.json")
    postgres_transactions.create_item(item, request=MockStarletteRequest)

    params = {"limit": 10001}
    resp = app_client.post("/search", json=params)
    assert resp.status_code == 400


def test_app_filter_extension_limit_10000(
    load_test_data, app_client, postgres_transactions
):
    item = load_test_data("test_item.json")
    postgres_transactions.create_item(item, request=MockStarletteRequest)

    params = {"limit": 10000}
    resp = app_client.post("/search", json=params)
    assert resp.status_code == 200


def test_app_sort_extension(load_test_data, app_client, postgres_transactions):
    # TODO: Rewrite this test, as postgres_transactions.create_item does not actually put
    # anything in the database
    # For now just check that the status code is 200
    first_item = load_test_data("test_item.json")
    item_date = datetime.strptime(
        first_item["properties"]["datetime"], "%Y-%m-%dT%H:%M:%SZ"
    )
    postgres_transactions.create_item(first_item, request=MockStarletteRequest)

    second_item = load_test_data("test_item.json")
    second_item["id"] = "another-item"
    another_item_date = item_date - timedelta(days=1)
    second_item["properties"]["datetime"] = another_item_date.strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    postgres_transactions.create_item(second_item, request=MockStarletteRequest)

    params = {
        "collections": [first_item["collection"]],
        "sortby": [{"field": "datetime", "direction": "desc"}],
    }
    resp = app_client.post("/search", json=params)
    assert resp.status_code == 200
    # resp_json = resp.json()
    # assert resp_json["features"][0]["id"] == first_item["id"]
    # assert resp_json["features"][1]["id"] == second_item["id"]


def test_search_invalid_date(load_test_data, app_client, postgres_transactions):
    item = load_test_data("test_item.json")
    postgres_transactions.create_item(item, request=MockStarletteRequest)

    params = {
        "datetime": "2020-XX-01/2020-10-30",
        "collections": [item["collection"]],
    }

    resp = app_client.post("/search", json=params)
    assert resp.status_code == 400


def test_search_point_intersects(load_test_data, app_client, postgres_transactions):
    item = load_test_data("test_item.json")
    postgres_transactions.create_item(item, request=MockStarletteRequest)

    point = [12.095, 55.26]
    intersects = {"type": "Point", "coordinates": point}

    params = {
        "intersects": intersects,
        "collections": [item["collection"]],
    }
    resp = app_client.post("/search", json=params)
    assert resp.status_code == 200
    resp_json = resp.json()
    assert len(resp_json["features"]) == 10  # TODO write a proper point intersection


def test_datetime_non_interval(load_test_data, app_client, postgres_transactions):
    item = load_test_data("test_item.json")
    postgres_transactions.create_item(item, request=MockStarletteRequest)

    alternate_formats = [
        "2017-05-27T09:04:49+00:00",
        "2017-05-27T09:04:49.00Z",
        "2017-05-27T09:04:49Z",
        "2017-05-27T09:04:49.00+00:00",
    ]
    for date in alternate_formats:
        params = {
            "datetime": date,
            "collections": [item["collection"]],
        }

        resp = app_client.post("/search", json=params)
        assert resp.status_code == 200
        resp_json = resp.json()
        assert len(resp_json["features"]) != 0
        # datetime is returned in this format "2017-05-27T09:04:49Z"
        assert resp_json["features"][0]["properties"]["datetime"][0:19] == date[0:19]


def test_bbox_3d(load_test_data, app_client, postgres_transactions):
    item = load_test_data("test_item.json")
    postgres_transactions.create_item(item, request=MockStarletteRequest)

    danish_bbox = [
        6.24,
        52.17,
        13.095,
        58.26,
    ]
    params = {"bbox": danish_bbox, "collections": ["skraafotos2017"]}
    resp = app_client.post("/search", json=params)
    assert resp.status_code == 200
    resp_json = resp.json()
    assert len(resp_json["features"]) == 10


def test_search_line_string_intersects(
    load_test_data, app_client, postgres_transactions
):
    item = load_test_data("test_item.json")
    postgres_transactions.create_item(item, request=MockStarletteRequest)

    line = [
        [11.249865714048164, 55.17886766328200],
        [
            13.095568839048,
            56.26776108,
        ],
    ]
    intersects = {"type": "LineString", "coordinates": line}

    params = {
        "intersects": intersects,
        "collections": [item["collection"]],
    }
    resp = app_client.post("/search", json=params)
    assert resp.status_code == 200
    resp_json = resp.json()
    assert len(resp_json["features"]) == 10


# Check that the hardcoded queryable names matches an equivalent in QueryableInfo, and in result property names
def test_filter_queryables_config(app_client, load_test_data):
    queryable_enums = list(BaseQueryables._member_names_) + list(
        SkraafotosProperties._member_names_
    )
    queryable_info = list([i for i in QueryableInfo.__dict__.keys() if i[:1] != "_"])

    assert len(queryable_enums) == len(queryable_info)
    for x, y in zip(queryable_enums, queryable_info):
        assert x == y

    test_item = load_test_data("test_item.json")
    queryable_enum_vals = list(BaseQueryables._value2member_map_) + list(
        SkraafotosProperties._value2member_map_
    )
    response_props = list(test_item.keys()) + list(test_item["properties"].keys())

    for q in queryable_enum_vals:
        q = q.split(".")[0]
        assert q in response_props


def test_filter_queryables_single_collection(app_client, load_test_data):
    resp = app_client.get(f"/collections/{test_item['collection']}/queryables")
    assert resp.status_code == 200


def test_filter_queryables_all_collections(app_client, load_test_data):
    """Test GET queryables without collection parameter returns intersection of queryables of all registered collections"""
    resp = app_client.get(f"/collections")
    resp_json = resp.json()

    all_queryables = []
    for coll in resp_json["collections"]:
        q = app_client.get(f"/collections/{coll['id']}/queryables")
        assert q.status_code == 200
        q_json = q.json()
        all_queryables.append(list(q_json["properties"].keys()))
    shared_queryables = set.intersection(*[set(x) for x in all_queryables])

    resp = app_client.get(f"/queryables")
    assert resp.status_code == 200
    resp_json = resp.json()
    assert len(resp_json["properties"]) == len(shared_queryables)


def test_app_path_allowing_token_should_return_links_with_token(
    load_test_data, token_app_client, postgres_transactions
):
    item = load_test_data("test_item.json")
    postgres_transactions.create_item(item, request=MockStarletteRequest)

    params = {"token": "TESTTOKEN"}

    for route in STAC_ROUTES_REQUIRING_TOKEN:
        path = route["path"].format(itemId=item["id"], collectionId=item["collection"])
        if route["method"] == "GET":
            resp = token_app_client.get(path, params=params)
        else:
            resp = token_app_client.post(path, json={}, params=params)
        assert resp.status_code == 200
        assert b"token=TESTTOKEN" in resp.content
