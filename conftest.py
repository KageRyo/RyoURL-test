import pytest
import requests
from urllib.parse import urljoin
from dotenv import load_dotenv
import os

# 載入 .env 文件
load_dotenv()

# 環境變數設定
BASE_URL = os.getenv("BASE_URL")
TEST_USER = {
    "username": os.getenv("TEST_USER_USERNAME"),
    "password": os.getenv("TEST_USER_PASSWORD")
}
ADMIN_USER = {
    "username": os.getenv("ADMIN_USER_USERNAME"),
    "password": os.getenv("ADMIN_USER_PASSWORD")
}

# 用來發送 HTTP 請求的客戶端類別
class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None

    # 登入
    def login(self, username, password):
        response = self.post("auth/login", json={"username": username, "password": password})
        if response.status_code == 200:
            self.token = response.json()["access"]  # 登入後將 access token 存起來
        return response

    # 發送 HTTP 請求
    def request(self, method, endpoint, **kwargs):
        url = urljoin(self.base_url, endpoint)
        headers = kwargs.pop("headers", {})
        # 如果有 token，則加入 Authorization 標頭（JWT 驗證）
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        response = requests.request(method, url, headers=headers, **kwargs)
        print(f"Request to {url}: Status {response.status_code}, Content: {response.text[:200]}")
        return response

    def get(self, endpoint, **kwargs):  # 發送 GET 請求
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs): # 發送 POST 請求
        return self.request("POST", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs): # 發送 DELETE 請求
        return self.request("DELETE", endpoint, **kwargs)

@pytest.fixture
def api_client():   # 用來建立 APIClient 實例的 fixture
    return APIClient(BASE_URL)

@pytest.fixture
def user_client(api_client):    # 用來建立一般使用者登入後的 APIClient 實例的 fixture
    api_client.login(TEST_USER["username"], TEST_USER["password"])
    return api_client

@pytest.fixture
def admin_client(api_client):   # 用來建立管理員登入後的 APIClient 實例的 fixture
    api_client.login(ADMIN_USER["username"], ADMIN_USER["password"])
    return api_client