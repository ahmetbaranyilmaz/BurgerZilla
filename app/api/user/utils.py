from marshmallow import Schema, fields


class UpdateModelSchema(Schema):
    """ /api/<str:username>/order/<int:order_id> [PUT]

    Parameters:
    - burger_id (int)
    - quantity (int)
    """

    burger_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True)


def validate_username(username: str, jwt_username: str) -> bool:
    return username == jwt_username
