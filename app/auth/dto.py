from flask_restx import Namespace, fields


class AuthDto:
    api = Namespace('auth', description='Authentication related operations')

    user_obj = api.model('User Object', {
        "email": fields.String,
        "name": fields.String,
        "username": fields.String,
        "joined_date": fields.DateTime,
        "is_restaurant": fields.Boolean
    })

    auth_login = api.model('Login Data', {
        "email": fields.String(required=True, description="User email address"),
        "password": fields.String(required=True, description="User password")
    })

    auth_register = api.model('Register Data', {
        "email": fields.String(required=True, description="User email address"),
        "username": fields.String(required=True, description="User username"),
        "name": fields.String(required=True, description="User name"),
        "password": fields.String(required=True, description="User password")
    })

    auth_restaurant = api.model("Register Restaurant Data", {
        "name": fields.String(required=True, description="Restaurant Name")
                                 })

    auth_success = api.model('Auth Success Response', {
        "status": fields.Boolean,
        "message": fields.String,
        "access_token": fields.String,
        "user": fields.Nested(user_obj)
    })
