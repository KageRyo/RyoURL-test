import random
import string
from locust import HttpUser, task, between
from locustfile import BASE_URL

def generate_random_string(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# 一般使用者
class AuthenticatedUser(HttpUser):
    host = BASE_URL
    wait_time = between(1, 5)
    
    # 開始時，先進行登入
    def on_start(self):
        self.login()
    
    def login(self):
        response = self.client.post("/auth/login", json={
            "username": "test_user_0000",
            "password": "test_user_pwd0"
        })
        if response.status_code == 200:
            data = response.json()
            self.token = data["access"]
            self.client.headers = {"Authorization": f"Bearer {self.token}"}
    
    # 短網址完整流程：建立、查詢、刪除
    @task(3)
    def short_url(self):
        # 建立自訂短網址
        custom_string = generate_random_string()
        data = {
            "origin_url": f"https://www.example.com/{random.randint(1, 1000)}",
            "short_string": custom_string
        }
        create_response = self.client.post("/short-url-with-auth/custom", json=data)
        
        if create_response.status_code == 201:
            # 查詢所有短網址
            get_response = self.client.get("/short-url-with-auth/all-my")
            
            if get_response.status_code == 200:
                # 刪除剛剛建立的短網址
                self.client.delete(f"/short-url-with-auth/url/{custom_string}")
    
    # 取得使用者資訊
    @task(1)
    def get_user_info(self):
        self.client.get("/user/info?username=test_user_0000")