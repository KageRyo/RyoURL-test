import pytest
from http import HTTPStatus

def test_anonymous_can_create_short_url(api_client):
    data = {"origin_url": "https://www.example.com"}
    response = api_client.post("short-url/short", json=data)
    assert response.status_code == HTTPStatus.CREATED
    #assert response.json()["creator_username"] == "anonymous"

def test_anonymous_can_get_original_url(api_client):
    # 首先創建一個短網址
    data = {"origin_url": "https://www.example.com"}
    create_response = api_client.post("short-url/short", json=data)
    short_string = create_response.json()["short_string"]

    # 然後獲取原始 URL
    response = api_client.get(f"short-url/origin/{short_string}")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["origin_url"] == "https://www.example.com/"
    #assert response.json()["creator_username"] == "anonymous"

def test_user_can_create_short_url(user_client):
    data = {"origin_url": "https://www.example.com"}
    response = user_client.post("short-url/short", json=data)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["creator_username"] == "test_user_0000"