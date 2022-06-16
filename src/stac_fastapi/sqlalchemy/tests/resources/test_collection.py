import pystac


def test_collection_not_found(app_client):
    """Test read a collection which does not exist"""
    resp = app_client.get("/collections/does-not-exist")
    assert resp.status_code == 404


def test_collection_items_collectionid_not_found(app_client, load_test_data):
    """Test read an item with a collectionId that does not exist"""
    test_collection = load_test_data("test_collection.json")
    test_item = load_test_data("test_item.json")

    # Test that we get a 404 if the collectionId does not exist
    resp = app_client.get(f"/collections/does-not-exist/items")
    assert resp.status_code == 404
    resp_json = resp.json()
    assert resp_json["detail"] == "Not found"

    # Test that we get a 404 if the itemId does not exist but the collectionId does
    resp = app_client.get(f"/collections/{test_collection['id']}/items/does-not-exist")
    assert resp.status_code == 404
    resp_json = resp.json()
    assert resp_json["detail"] == "Not found"

    # Test that we get a 404 if the collectionId does not exist but the itemId does
    resp = app_client.get(f"/collections/does-not-exist/items/{test_item['id']}")
    assert resp.status_code == 404
    resp_json = resp.json()
    assert resp_json["detail"] == "Not found"

    # Test that we get a 404 if neither the itemId or the collectionId exists
    resp = app_client.get(f"/collections/does-not-exist/items/also-does-not-exist")
    assert resp.status_code == 404
    resp_json = resp.json()
    assert resp_json["detail"] == "Not found"

    ## finally check that we get the item if both exists
    resp = app_client.get(
        f"/collections/{test_collection['id']}/items/{test_item['id']}"
    )
    assert resp.status_code == 200


def test_returns_valid_collection(app_client, load_test_data):
    """Test validates fetched collection with jsonschema"""
    test_collection = load_test_data("test_collection.json")
    resp = app_client.put("/collections", json=test_collection)
    assert resp.status_code == 200

    resp = app_client.get(f"/collections/{test_collection['id']}")
    assert resp.status_code == 200
    resp_json = resp.json()

    # Mock root to allow validation
    mock_root = pystac.Catalog(
        id="test", description="test desc", href="https://example.com"
    )
    collection = pystac.Collection.from_dict(
        resp_json, root=mock_root, preserve_dict=False
    )
    collection.validate()
