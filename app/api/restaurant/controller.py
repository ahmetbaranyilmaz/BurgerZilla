from flask_restx import Resource
from flask_jwt_extended import jwt_required
from flask import request
from .service import RestaurantService
from .dto import RestaurantDto
from .utils import InsertBurgerSchema, UpdateBurgerSchema, UpdateOrderSchema
from app.utils import validation_error

insert_schema = InsertBurgerSchema()
update_burger_schema = UpdateBurgerSchema()
update_order_schema = UpdateOrderSchema()

api = RestaurantDto.api
data_resp = RestaurantDto.data_resp
restaurant = RestaurantDto.restaurant
burger = RestaurantDto.burger
update_burger = RestaurantDto.update_burger
update_order = RestaurantDto.update_order


@api.route("")
class RestaurantsGet(Resource):
    @api.doc("List All Restaurants", responses={
        200: ("Success", data_resp),
        404: 'Restaurant Not Found',
    })
    def get(self) -> dict:
        """
        List All Restaurants
        """
        return RestaurantService.get_restaurants()


@api.route("/<int:res_id>/menu")
class RestaurantMenu(Resource):
    @api.doc("List Selected Restaurant Menu", responses={
        200: "Success",
        404: 'Restaurant Not Found',
    })
    def get(self, res_id: int) -> dict:
        """
        List Selected Restaurant Menu
        :param res_id:
        """
        return RestaurantService.get_restaurant_menu(res_id)

    @api.doc("Insert New Burger to Menu", responses={
        200: 'Burger Insert Success',
        404: 'Burger Not Found',
        400: 'Unauthorized Access'
    })
    @jwt_required()
    @api.expect(burger, validate=True)
    def post(self, res_id: int):
        """
         Insert new burger to menu. Need to be owner of restaurant
        :param res_id:
        """
        data = request.get_json()
        if errors := insert_schema.validate(data):
            return validation_error(False, errors), 400
        return RestaurantService.insert_burger(res_id, data)


@api.route("/<int:res_id>/menu/<int:burger_id>")
class RestaurantBurger(Resource):
    @api.doc("Get Burger Detail", responses={
        200: "Success",
        404: "Burger Not Found",
    })
    def get(self, res_id: int, burger_id: int) -> dict:
        """
        Lists burger detail of selected burger
        :param res_id:
        :param burger_id:
        """
        return RestaurantService.get_restaurant_burger(res_id, burger_id)

    @api.doc("Update Burger", responses={
        200: "Success",
        404: "Burger Not Found",
        400: "Unauthorized Access"
    })
    @jwt_required()
    @api.expect(update_burger, validate=True)
    def put(self, res_id: int, burger_id: int):
        """
        Updates Burger detail. Need to be owner of restaurant
        :param res_id:
        :param burger_id:
        """

        data = request.get_json()

        if errors := update_burger_schema.validate(data):
            return validation_error(False, errors), 400

        return RestaurantService.update_restaurant_burger(res_id, burger_id, data)

    @api.doc("Delete Burger", responses={
        200: "Success",
        404: "Order Not Found",
        400: "Unauthorized Access"
    })
    @jwt_required()
    def delete(self, res_id: int, burger_id: int) -> dict:
        """
        Deletes burger from menu. Need to be owner of restaurant
        :param res_id:
        :param burger_id:
        """
        return RestaurantService.delete_restaurant_burger(res_id, burger_id)


@api.route("/<int:res_id>/orders")
class RestaurantOrder(Resource):
    @api.doc("Get Restaurant Orders", responses={
        200: "Success",
        404: "Order Not Found",
        400: "Unauthorized Access"
    })
    @jwt_required()
    def get(self, res_id: int) -> dict:
        """
        List all orders restaurant have. Need to be owner of restaurant
        :param res_id:
        """
        return RestaurantService.get_restaurant_orders(res_id)


@api.route("/<int:res_id>/order/<int:order_id>")
class RestaurantOrderDetail(Resource):
    @api.doc("Get Order Detail", responses={
        200: "Success",
        404: "Order Not Found",
        400: "Unauthorized Access"
    })
    @jwt_required()
    def get(self, res_id: int, order_id: int) -> dict:
        """
        List order detail of specified order. Need to be owner of restaurant
        :param res_id:
        :param order_id:
        """
        return RestaurantService.get_restaurant_order_detail(res_id, order_id)

    @api.doc("Update order", responses={
        200: "Success",
        404: "Order Not Found",
        400: "Unauthorized Access"
    })
    @jwt_required()
    @api.expect(update_order, validate=True)
    def put(self, res_id: int, order_id: int):
        """
        Update order. Need to be owner of restaurant
        :param res_id:
        :param order_id:
        """

        data = request.get_json()
        if errors := update_order_schema.validate(data):
            return validation_error(False, errors), 400
        return RestaurantService.update_restaurant_order(res_id, order_id, data)

    @api.doc("Delete order", responses={
        200: "Success",
        404: "Order Not Found",
        400: "Unauthorized Access"
    })
    @jwt_required()
    def delete(self, res_id: int, order_id: int) -> dict:
        """
        Delete order. Need to be owner of restaurant
        :param res_id:
        :param order_id:
        """
        return RestaurantService.delete_restaurant_order(res_id, order_id)
