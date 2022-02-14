from flask_restx import Namespace, fields


class UserDto:
    api = Namespace("<string:username>", description="User Related Operations")

    user = api.model("User Model", {
        "email": fields.String,
        "name": fields.String,
        "username": fields.String,
        "joined_date": fields.DateTime,
        "is_restaurant": fields.Boolean
    })

    data_resp = api.model("User Data Response", {
        "status": fields.Boolean,
        "message": fields.String,
        "user": fields.Nested(user)
    })

    update_model = api.model('Burger Model - Update', {
        'burger_id': fields.Integer(description="Selected Burger id"),
        'quantity': fields.Integer(description="Burger quantity")
    })

    order_model = api.model('Burger Model - Insert', {
        'burgers': fields.List(fields.Nested(
            update_model
        ))
    })
