import pytest
from http import HTTPStatus
from schemas.schemas import UrlSchema, UserInfoSchema, ErrorSchema
from typing import List

"""
管理員使用管理員 API 測試
"""
# GET /admin/all-urls 取得所有短網址
def test_admin_can_access_all_urls(admin_client):
    response = admin_client.get("admin/all-urls")
    assert response.status_code == HTTPStatus.OK
    urls = [UrlSchema(**url) for url in response.json()]
    assert isinstance(urls, list)

# DELETE /admin/expire-urls 刪除過期短網址
def test_admin_can_expire_urls(admin_client):
    response = admin_client.delete("admin/expire-urls")
    assert response.status_code == HTTPStatus.NO_CONTENT

# GET /admin/users 取得所有使用者資訊
def test_admin_can_get_all_users(admin_client):
    response = admin_client.get("admin/users")
    assert response.status_code == HTTPStatus.OK
    users = [UserInfoSchema(**user) for user in response.json()]
    assert isinstance(users, list)
    assert len(users) > 0

# PUT /admin/user/{username} 更新使用者身分
def test_admin_can_update_user_type(admin_client):
    response = admin_client.put("admin/user/test_user_0000", params={"user_type": 1})
    assert response.status_code == HTTPStatus.OK
    user = UserInfoSchema(**response.json())
    assert user.username == "test_user_0000"
    assert user.user_type == 1

"""
一般使用者使用管理員 API 測試
"""    
# 一般使用者不應該可以使用任何管理員 API
def test_user_cannot_access_all_urls(user_client):
    response = user_client.get("admin/all-urls")
    assert response.status_code == HTTPStatus.FORBIDDEN
    ErrorSchema(detail=response.json()["detail"])

def test_user_cannot_expire_urls(user_client):
    response = user_client.delete("admin/expire-urls")
    assert response.status_code == HTTPStatus.FORBIDDEN
    ErrorSchema(detail=response.json()["detail"])

def test_user_cannot_get_all_users(user_client):
    response = user_client.get("admin/users")
    assert response.status_code == HTTPStatus.FORBIDDEN
    ErrorSchema(detail=response.json()["detail"])

def test_user_cannot_update_user_type(user_client):
    response = user_client.put("admin/user/test_user_0000", params={"user_type": 1})
    assert response.status_code == HTTPStatus.FORBIDDEN
    ErrorSchema(detail=response.json()["detail"])