from flask_restx import Namespace, fields


class RestaurantDto:
    api = Namespace('restaurant', description='Restaurant Related Operations')

    restaurant = api.model('Restaurant', {
        'res_id': fields.Integer,
        'name': fields.String,
        'user_id': fields.String,
    })

    burger = api.model('Burger Model - Insert', {
        'name': fields.String(description='Burger Name'),
        'price': fields.Integer(description='Burger Price'),
        'description': fields.String(description='Burger Description'),
        'image_path': fields.String(description='Burger Image Path')
    })

    update_burger = api.model('Burger Model - Update', {
        'name': fields.String(description='Burger Name'),
        'price': fields.Integer(description='Burger Price'),
        'description': fields.String(description='Burger Description'),
        'image_path': fields.String(description='Burger Image Path'),
        'is_active': fields.Boolean(description='Burger Is Active')
    })

    update_order = api.model("Order Model - Update", {
        'status_id': fields.Integer(description='Status id= 0:PREPARING, 1:ON_THE_WAY, 2:DELIVERED, 3:CANCELLED')
    })

    data_resp = api.model('Response Data', {
        'status': fields.Boolean,
        'message': fields.String,
        'restaurant': fields.Nested(restaurant)
    })
