from app.models.restaurant import Restaurant
from marshmallow import Schema, fields
from marshmallow.validate import OneOf


class InsertBurgerSchema(Schema):
    """ /api/restaurant>/<int:res_d>/menu [POST]

    Parameters:
    - name (Str)
    - price (int)
    - description (Str)
    - image_path (Str)
    """

    name = fields.String(required=True)
    price = fields.Integer(required=True)
    description = fields.String(required=True)
    image_path = fields.String(required=True)


class UpdateBurgerSchema(Schema):
    """ /api/restaurant>/<int:res_d>/menu [POST]

    Parameters:
    - name (Str)
    - price (int)
    - description (Str)
    - image_path (Str)
    - is_active (bool)
    """

    name = fields.String(required=True)
    price = fields.Integer(required=True)
    description = fields.String(required=True)
    image_path = fields.String(required=True)
    is_active = fields.Boolean(required=True)


class UpdateOrderSchema(Schema):
    """ /api/restaurant>/<int:res_d>/menu [POST]

    Parameters:
    - status_id (int)
    """

    status_id = fields.Integer(required=True, validate=[
        OneOf([0, 1, 2, 3, 4])
    ])


def validate_restaurant_owner(res_id: int, jwt_user_id: int) -> bool:
    user_id_test = Restaurant.query.get(res_id).get_user_id()
    return user_id_test == jwt_user_id


def validate_restaurant(current_user: dict, res_id: int) -> bool:
    user_id = current_user["user_id"]
    is_restaurant = current_user["is_restaurant"]

    return is_restaurant and validate_restaurant_owner(res_id, user_id)

