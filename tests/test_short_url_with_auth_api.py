import pytest
import random
import string
from http import HTTPStatus

def generate_random_string(length=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def test_anonymous_cannot_create_custom_url(api_client):
    data = {"origin_url": "https://www.example.com", "short_string": "custom"}
    response = api_client.post("short-url-with-auth/custom", json=data)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

def test_anonymous_cannot_get_all_my_urls(api_client):
    response = api_client.get("short-url-with-auth/all-my")
    assert response.status_code == HTTPStatus.UNAUTHORIZED

def test_user_can_create_custom_url(user_client):
    custom_string = generate_random_string()
    data = {"origin_url": "https://www.example.com", "short_string": custom_string}
    response = user_client.post("short-url-with-auth/custom", json=data)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["short_string"] == custom_string
    assert response.json()["creator_username"] == "test_user_0000"

def test_user_can_get_all_my_urls(user_client):
    response = user_client.get("short-url-with-auth/all-my")
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), list)
    for url in response.json():
        assert url["creator_username"] == "test_user_0000"

def test_user_can_delete_own_url(user_client):
    # 首先創建一個短網址
    data = {"origin_url": "https://www.example.com", "short_string": "todelete"}
    create_response = user_client.post("short-url-with-auth/custom", json=data)
    short_string = create_response.json()["short_string"]

    # 然後刪除這個短網址
    response = user_client.delete(f"short-url-with-auth/url/{short_string}")
    assert response.status_code == HTTPStatus.NO_CONTENT

    # 確認短網址已被刪除
    get_response = user_client.get(f"short-url/origin/{short_string}")
    assert get_response.status_code == HTTPStatus.NOT_FOUND

def test_admin_create_custom_short_url(admin_client):
    data = {"origin_url": "https://www.example.com", "short_string": "adminurl"}
    response = admin_client.post("short-url-with-auth/custom", json=data)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["short_string"] == "adminurl"
    assert response.json()["creator_username"] == "test_admin_0000"

def test_user_delete_others_short_url(user_client):
    response = user_client.delete("short-url-with-auth/url/adminurl")
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json()["detail"] == "無權限刪除此短網址"
    
def test_admin_delete_user_short_url(admin_client):
    response = admin_client.delete("short-url-with-auth/url/adminurl")
    assert response.status_code == HTTPStatus.NO_CONTENT