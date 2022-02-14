from datetime import datetime
from email import message
from flask import current_app
from flask_jwt_extended import create_access_token, get_jwt_identity

from app import db
from app.utils import message, err_resp, internal_err_resp
from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.schemas import UserSchema
from app.models.schemas import RestaurantSchema

restaurant_schema = RestaurantSchema()
user_schema = UserSchema()


class AuthService:
    @staticmethod
    def login(data: dict):
        email = data.get('email')
        password = data.get('password')
        try:
            if not (user := User.query.filter_by(email=email).first()):
                return err_resp('Email not exist', "email_404", 404)
            elif user and user.verify_password(password):
                identity = {
                    "user_id": user.user_id,
                    "username": user.username,
                    "is_restaurant": user.is_restaurant
                }
                access_token = create_access_token(identity=identity)
                resp = message('True', 'Login Success')
                resp['access_token'] = access_token

                user_info = user_schema.dump(user)
                resp['user'] = user_info
                return resp, 200
            return err_resp('Wrong email or password', "email_password_404", 404)

        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def register(data: dict):
        email = data.get('email')
        username = data.get('username')
        name = data.get('name')
        password = data.get('password')

        if User.query.filter_by(email=email).first():
            return err_resp('This email is used', "email_409", 409)
        elif User.query.filter_by(username=username).first():
            return err_resp('This username is used', "username_409", 409)

        try:
            user = User(email=email,
                        username=username,
                        name=name,
                        password=password,
                        joined_date=datetime.utcnow())
            db.session.add(user)
            db.session.commit()

            identity = {
                "user_id": user.user_id,
                "username": username,
                "is_restaurant": user.is_restaurant
            }

            access_token = create_access_token(identity=identity)
            resp = message('True', 'Register success')
            resp['access_token'] = access_token
            user_info = user_schema.dump(user)
            resp['user'] = user_info
            return resp, 200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def register_restaurant(data: dict):
        current_user = get_jwt_identity()
        user_id = current_user.get("user_id")
        username = current_user.get("username")

        name = data.get("name")

        user = User.query.get(user_id)
        user_data = user_schema.dump(user)

        if user_data["is_restaurant"]:
            return err_resp("You have restaurant", "restaurant_409", 409)

        try:
            restaurant = Restaurant(
                name=name,
                user_id=user_id
            )
            db.session.add(restaurant)
            User.query.filter_by(user_id=user_id).update({"is_restaurant": True})
            db.session.commit()
            identity = {
                "user_id": user_id,
                "username": username,
                "is_restaurant": True
            }
            access_token = create_access_token(identity=identity)
            resp = message('True', 'Register success')
            resp['access_token'] = access_token
            restaurant_info = restaurant_schema.dump(restaurant)
            resp['user'] = restaurant_info

            return resp, 200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()
