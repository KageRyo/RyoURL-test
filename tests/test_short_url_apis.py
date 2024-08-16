import pytest
from http import HTTPStatus
from schemas.schemas import UrlSchema

"""
無需認證的短網址 API 測試
"""

# GET /short-url/origin/{short_string} 取得原始網址
def test_anonymous_can_get_original_url(api_client):
    # 首先創建一個短網址
    data = {"origin_url": "https://www.example.com"}
    create_response = api_client.post("short-url/short", json=data)
    short_string = UrlSchema(**create_response.json()).short_string

    # 然後獲取原始 URL
    response = api_client.get(f"short-url/origin/{short_string}")
    assert response.status_code == HTTPStatus.OK
    
    url_data = UrlSchema(**response.json())
    assert str(url_data.origin_url) == "https://www.example.com/"
    assert url_data.creator_username == "anonymous"

# POST /short-url/short 創建短網址 (匿名用戶)
def test_anonymous_can_create_short_url(api_client):
    data = {"origin_url": "https://www.example.com"}
    response = api_client.post("short-url/short", json=data)
    assert response.status_code == HTTPStatus.CREATED
    
    # 使用 UrlSchema 驗證回應
    url_data = UrlSchema(**response.json())
    assert str(url_data.origin_url) == "https://www.example.com/"
    assert url_data.creator_username == "anonymous"

# POST /short-url/short 創建短網址 (已登入用戶)
def test_user_can_create_short_url(user_client):
    data = {"origin_url": "https://www.example.com"}
    response = user_client.post("short-url/short", json=data)
    assert response.status_code == HTTPStatus.CREATED
    
    url_data = UrlSchema(**response.json())
    assert url_data.creator_username == "test_user_0000"