import pytest
import random
import string
from http import HTTPStatus
from schemas.schemas import UrlSchema, ErrorSchema, CustomUrlCreateSchema

def generate_random_string(length=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

"""
需要認證的短網址 API 測試
"""

# POST /short-url-with-auth/custom 創建自定義短網址 (匿名用戶)
def test_anonymous_cannot_create_custom_url(api_client):
    data = CustomUrlCreateSchema(origin_url="https://www.example.com", short_string="custom")
    response = api_client.post("short-url-with-auth/custom", json={
        "origin_url": str(data.origin_url),
        "short_string": data.short_string
    })
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    ErrorSchema(message=response.json()["detail"])

# GET /short-url-with-auth/all-my 取得所有自己的短網址 (匿名用戶)
def test_anonymous_cannot_get_all_my_urls(api_client):
    response = api_client.get("short-url-with-auth/all-my")
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    ErrorSchema(message=response.json()["detail"])

# POST /short-url-with-auth/custom 創建自定義短網址 (已登入用戶)
def test_user_can_create_custom_url(user_client):
    custom_string = generate_random_string()
    data = CustomUrlCreateSchema(origin_url="https://www.example.com", short_string=custom_string)
    response = user_client.post("short-url-with-auth/custom", json={
        "origin_url": str(data.origin_url),
        "short_string": data.short_string
    })
    assert response.status_code == HTTPStatus.CREATED
    url = UrlSchema(**response.json())
    assert url.short_string == custom_string
    assert url.creator_username == "test_user_0000"

# GET /short-url-with-auth/all-my 取得所有自己的短網址 (已登入用戶)
def test_user_can_get_all_my_urls(user_client):
    response = user_client.get("short-url-with-auth/all-my")
    assert response.status_code == HTTPStatus.OK
    urls = [UrlSchema(**url) for url in response.json()]
    assert isinstance(urls, list)
    for url in urls:
        assert url.creator_username == "test_user_0000"

# DELETE /short-url-with-auth/url/{short_string} 刪除短網址 (已登入用戶)
def test_user_can_delete_own_url(user_client):
    # 首先創建一個短網址
    custom_string = generate_random_string(10)  # 生成 10 個字符的隨機字符串
    data = CustomUrlCreateSchema(origin_url="https://www.example.com", short_string=custom_string)
    create_response = user_client.post("short-url-with-auth/custom", json={
        "origin_url": str(data.origin_url),
        "short_string": data.short_string
    })
    assert create_response.status_code == HTTPStatus.CREATED, f"Failed to create URL: {create_response.json()}"

    url_data = UrlSchema(**create_response.json())
    short_string = url_data.short_string

    # 然後刪除這個短網址
    response = user_client.delete(f"short-url-with-auth/url/{short_string}")
    assert response.status_code == HTTPStatus.NO_CONTENT

    # 確認短網址已被刪除
    response = user_client.delete(f"short-url-with-auth/url/{short_string}")
    assert response.status_code == HTTPStatus.NOT_FOUND

# POST /short-url-with-auth/custom 創建自定義短網址 (管理員)
def test_admin_create_custom_short_url(admin_client):
    data = CustomUrlCreateSchema(origin_url="https://www.example.com", short_string="adminurl")
    response = admin_client.post("short-url-with-auth/custom", json={
        "origin_url": str(data.origin_url),
        "short_string": data.short_string
    })
    assert response.status_code == HTTPStatus.CREATED
    url = UrlSchema(**response.json())
    assert url.short_string == "adminurl"
    assert url.creator_username == "test_admin_0000"

# DELETE /short-url-with-auth/url/{short_string} 刪除短網址 (一般用戶刪除他人的網址)
def test_user_delete_others_short_url(user_client):
    response = user_client.delete("short-url-with-auth/url/adminurl")
    assert response.status_code == HTTPStatus.FORBIDDEN
    ErrorSchema(message=response.json()["detail"])
    
# DELETE /short-url-with-auth/url/{short_string} 刪除短網址 (管理員刪除任何人的網址)
def test_admin_delete_user_short_url(admin_client):
    response = admin_client.delete("short-url-with-auth/url/adminurl")
    assert response.status_code == HTTPStatus.NO_CONTENT