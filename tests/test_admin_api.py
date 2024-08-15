import pytest
from http import HTTPStatus

# 測試管理員可以訪問所有 URL
def test_admin_can_access_all_urls(admin_client):
    response = admin_client.get("admin/all-urls")
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), list)

# 測試管理員可以刪除過期的 URL
def test_admin_can_expire_urls(admin_client):
    response = admin_client.delete("admin/expire-urls")
    assert response.status_code == HTTPStatus.NO_CONTENT

# 測試管理員可以獲取所有用戶信息
def test_admin_can_get_all_users(admin_client):
    response = admin_client.get("admin/users")
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), list)

# 測試管理員可以更新用戶類型
def test_admin_can_update_user_type(admin_client):
    response = admin_client.put("admin/user/test_user_0000", params={"user_type": 1})
    assert response.status_code == HTTPStatus.OK
    assert response.json()["username"] == "test_user_0000"
    assert response.json()["user_type"] == 1
    
# 測試普通用戶無法訪問所有 URL
def test_user_cannot_access_all_urls(user_client):
    response = user_client.get("admin/all-urls")
    assert response.status_code == HTTPStatus.FORBIDDEN

# 測試普通用戶無法刪除過期的 URL
def test_user_cannot_expire_urls(user_client):
    response = user_client.delete("admin/expire-urls")
    assert response.status_code == HTTPStatus.FORBIDDEN

# 測試普通用戶無法獲取所有用戶信息
def test_user_cannot_get_all_users(user_client):
    response = user_client.get("admin/users")
    assert response.status_code == HTTPStatus.FORBIDDEN

# 測試普通用戶無法更新用戶類型
def test_user_cannot_update_user_type(user_client):
    response = user_client.put("admin/user/test_user_0000", params={"user_type": 1})
    assert response.status_code == HTTPStatus.FORBIDDEN