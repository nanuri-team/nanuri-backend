import random

from faker import Faker
from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(5, 15)
    fake = Faker()

    def on_start(self):
        response = self.client.post(
            "http://localhost:8000/api/auth/token/",
            {"email": "admin@example.com", "password": "password1234"},
        )
        access_token = response.json()["access"]
        self.client.headers = {"Authorization": f"Bearer {access_token}"}

    @task
    def get_posts(self):
        self.client.get("http://localhost:8000/api/v1/posts/")

    @task
    def create_posts(self):
        self.client.post(
            "http://localhost:8000/api/v1/posts/",
            json={
                "title": self.fake.pystr(),
                "category": random.choice(
                    ["BATHROOM", "FOOD", "KITCHEN", "HOUSEHOLD", "STATIONERY", "ETC"]
                ),
                "unit_price": random.randint(1000, 100000),
                "quantity": random.randint(1, 100),
                "description": self.fake.paragraph(),
                "min_participants": random.randint(1, 10),
                "max_participants": random.randint(20, 100),
                "product_url": self.fake.image_url(),
                "trade_type": random.choice(["DIRECT", "PARCEL"]),
                "order_status": "WAITING",
                "is_published": True,
            },
        )
