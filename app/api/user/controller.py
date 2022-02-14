from flask_restx import Resource
from flask_jwt_extended import jwt_required
from flask import request
from .service import UserService
from .dto import UserDto
from .utils import UpdateModelSchema
from app.utils import validation_error

update_schema = UpdateModelSchema()

api = UserDto.api
data_resp = UserDto.data_resp
order_model = UserDto.order_model
update_model = UserDto.update_model


@api.route("")
class UserGet(Resource):
    @api.doc("Get Specified User Data", responses={
        200: ("Success", data_resp),
        404: "User Not Found",
        400: "Unauthorized Access"
    })
    @jwt_required()
    def get(self, username: str):
        """
        Get user info
        :param username:
        """
        return UserService.get_user_data(username)


@api.route("/orders")
class UserOrdersGet(Resource):
    @api.doc("Get User All Orders", responses={
        200: "Success",
        404: "User Not Found",
        400: "Unauthorized Access"
    })
    @jwt_required()
    def get(self, username: str):
        """
        List all orders from user. Need login
        :param username:
        """
        return UserService.get_user_orders(username)

    @api.doc("Give Order", responses={
        200: "Success",
        404: "Burger Not Found",
        400: "Unauthorized Access"
    })
    @jwt_required()
    @api.expect(order_model)
    def post(self, username: str):
        """
        Gives order. Need login
        :param username:
        """

        data = request.get_json()
        return UserService.insert_user_order(username, data)


@api.route("/order/<int:order_id>")
class UserOrderChanges(Resource):
    @api.doc("Get Order Detail", responses={
        200: "Success",
        404: "Order Not Found",
        400: "Unauthorized Access"
    })
    @jwt_required()
    def get(self, username: str, order_id: int):
        """
        Get selected order's detail. Need login
        :param username:
        :param order_id:
        """
        return UserService.get_user_order_detail(username, order_id)

    @api.doc("Delete Selected Order", responses={
        200: "Success",
        404: "Order Not Found",
        400: "Unauthorized Access"
    })
    @jwt_required()
    def delete(self, username: str, order_id: int):
        """
        Cancel order. Need login
        :param username:
        :param order_id:
        :return:
        """
        return UserService.delete_order(username, order_id)

    @api.doc("Update Selected Order", responses={
        200: "Success",
        404: "Order Not Found",
        400: "Unauthorized Access"
    })
    @jwt_required()
    @api.expect(update_model, validate=True)
    def put(self, username: str, order_id: int):
        """
        Update selected order
        :param username:
        :param order_id:
        """
        data = request.get_json()
        if errors := update_schema.validate(data):
            return validation_error(False, errors), 400
        return UserService.update_order(username, order_id, data)
