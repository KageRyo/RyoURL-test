import pytest
import uuid
from conftest import TEST_USER

# 測試使用者註冊（成為一般使用者）
def test_register(api_client):
    username = f"testuser_{uuid.uuid4().hex[:8]}"
    password = "testpassword123"
    # 註冊
    response = api_client.post("auth/register", json={
        "username": username,
        "password": password
    })
    # 測試項目：註冊成功後，回傳的 JSON 中應該包含 username, access, refresh 三個鍵，且 status code 應為 201
    assert response.status_code == 201, f"Register failed: {response.text}"
    data = response.json()
    assert "username" in data
    assert "access" in data
    assert "refresh" in data
    
# 測試使用者登入
def test_login(api_client):
    # 登入
    response = api_client.post("auth/login", json={
        "username": TEST_USER["username"],
        "password": TEST_USER["password"]
    })
    # 測試項目：登入成功後，回傳的 JSON 中應該包含 username, access, refresh 三個鍵，且 status code 應為 200
    assert response.status_code == 200, f"Login failed: {response.text}"
    data = response.json()
    assert "username" in data
    assert "access" in data
    assert "refresh" in data

# 測試更新 TOKEN
def test_refresh_token(api_client):
    # 登入並取得 refresh token
    login_response = api_client.post("auth/login", json={
        "username": TEST_USER["username"],
        "password": TEST_USER["password"]
    })
    # 測試項目：登入成功後，回傳的 JSON 中應該包含 refresh 鍵，且 status code 應為 200
    assert login_response.status_code == 200, f"Login failed: {login_response.text}"
    # 使用 refresh token 更新 access token
    refresh_token = login_response.json()["refresh"]
    refresh_response = api_client.post("auth/refresh-token", json={"refresh": refresh_token})
    # 測試項目：更新成功後，回傳的 JSON 中應該包含 access 鍵，且 status code 應為 200
    assert refresh_response.status_code == 200, f"Refresh token failed: {refresh_response.text}"
    data = refresh_response.json()
    assert "access" in data

# 測試登入失敗（輸入錯誤的帳號資料）
def test_login_failure(api_client):
    # 登入
    response = api_client.post("auth/login", json={
        "username": "wronguser",
        "password": "wrongpassword"
    })
    # 測試項目：登入失敗後，status code 應為 400，且回傳的 JSON 中應該包含 message 鍵
    assert response.status_code == 400, f"Expected 400, got {response.status_code}: {response.text}"
    data = response.json()
    assert "message" in data, f"Expected 'message' in response, got: {data}"