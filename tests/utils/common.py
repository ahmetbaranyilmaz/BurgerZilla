import json

from flask_jwt_extended import create_access_token

from app.models.burger import Burger
from app.models.restaurant import Restaurant
from app import db


def register_user(self, data: dict):
    return self.client.post(
        "/auth/register", data=json.dumps(data), content_type="application/json",
    )


def register_restaurant(self, data: dict, access_token):
    return self.client.post(
        "/auth/register/restaurant",
        data=json.dumps(data),
        content_type="application/json",
        headers={"Authorization": "Bearer " + access_token}
    )


def login_user(self, email: str, password: str):
    return self.client.post(
        "/auth/login",
        data=json.dumps(dict(email=email, password=password)),
        content_type="application/json",
    )
