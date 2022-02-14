from flask import current_app
from flask_jwt_extended import get_jwt_identity
from app.utils import err_resp, internal_err_resp, message, validation_error
from .utils import validate_restaurant
from app.models.restaurant import Restaurant
from app.models.burger import Burger
from app.models.order import Order
from app.models.order_detail import OrderDetail
from app.models.schemas import RestaurantSchema, BurgerSchema, UserSchema, OrderSchema
from app.models.schemas import OrderDetailSchema
from app import db
from app.constants.status import STATUS

order_detail_schema = OrderDetailSchema()
res_schema = RestaurantSchema()
burger_schema = BurgerSchema()
user_schema = UserSchema()
order_schema = OrderSchema()


class RestaurantService:
    @staticmethod
    def get_restaurants():
        """
        List all restaurants.
        """
        if not (restaurants := Restaurant.query.filter_by(is_active=True)):
            return err_resp(msg="Restaurants not found", code=404, reason="no_restaurants")

        try:
            resp = message(True, "Restaurants loaded successfully")
            resp["restaurants"] = [res_schema.dump(restaurant) for restaurant in restaurants]

            return resp, 200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def get_restaurant_menu(res_id: int):
        """
        List selected restaurant menu.
        """

        if not (restaurant := Restaurant.query.get(res_id)):
            return err_resp(msg="Restaurant not found", code=404, reason="no_restaurants")

        try:
            res_info = res_schema.dump(restaurant)
            res_name = res_info["name"]

            burgers = Burger.query.filter_by(res_id=res_id, is_active=True)
            menu = [burger_schema.dump(burger) for burger in burgers]

            resp = message(True, "Restaurant Menu loaded successfully")
            resp["res_name"] = res_name
            resp["menu"] = menu
            return resp, 200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def insert_burger(res_id: int, data: dict):
        """
        Insert burger to selected menu
        """
        current_user = get_jwt_identity()

        try:
            if not validate_restaurant(current_user, res_id):
                return validation_error(False, "Unauthorized Access"), 400
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

        try:
            burger = Burger(
                name=data["name"],
                price=data["price"],
                description=data["description"],
                image_path=data["image_path"],
                res_id=res_id
            )

            db.session.add(burger)
            db.session.commit()
            return message(True, "Burger added to menu successfully"), 200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def get_restaurant_burger(res_id: int, burger_id: int):
        if not (burger := Burger.query.get(burger_id)):
            return err_resp(msg="Burger not found", code=404, reason="no_burger")

        if not (restaurant := Restaurant.query.get(res_id)):
            return err_resp(msg="Restaurant not found", code=404, reason="no_restaurant")

        try:
            burger_info = burger_schema.dump(burger)
            res_info = res_schema.dump(restaurant)
            res_name = res_info["name"]

            resp = message(True, "Burger loaded successfully")
            resp["burger"] = burger_info
            resp["res_name"] = res_name
            return resp, 200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def update_restaurant_burger(res_id: int, burger_id: int, data: dict):
        current_user = get_jwt_identity()

        try:
            if not validate_restaurant(current_user, res_id):
                return validation_error(False, "Unauthorized Access"), 400
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

        if not (burger := Burger.query.get(burger_id)):
            return err_resp(msg="Burger not found", code=404, reason="no_burger")

        burger_info = burger_schema.dump(burger)
        if burger_info["res_id"] != res_id:
            return validation_error(False, "Unauthorized Access"), 400

        try:
            burger.name = data["name"]
            burger.price = data["price"]
            burger.is_active = data["is_active"]
            burger.description = data["description"]
            burger.image_path = data["image_path"]
            db.session.commit()
            resp = message(True, "Burger updated successfully")
            return resp, 200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def delete_restaurant_burger(res_id: int, burger_id: int):
        current_user = get_jwt_identity()

        try:
            if not validate_restaurant(current_user, res_id):
                return validation_error(False, "Unauthorized Access"), 400
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

        if not (burger := Burger.query.filter_by(burger_id=burger_id, is_active=True).first()):
            return err_resp(msg="Burger not found", code=404, reason="no_burger")

        burger_info = burger_schema.dump(burger)
        if burger_info["res_id"] != res_id:
            return validation_error(False, "Unauthorized Access"), 400

        try:
            burger.is_active = False
            db.session.commit()
            resp = message(True, "Burger deleted successfully")
            return resp, 200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def get_restaurant_orders(res_id: int):
        current_user = get_jwt_identity()

        try:
            if not validate_restaurant(current_user, res_id):
                return validation_error(False, "Unauthorized Access"), 400
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

        if not (orders := Order.query.filter_by(res_id=res_id, is_active=True)):
            return err_resp(msg="Order not found", code=404, reason="no_order")

        try:
            orders_info = []
            for order in orders:
                order_info = order_schema.dump(order)
                order_info["status"] = order.get_status().name
                orders_info.append(order_info)

            resp = message(True, "Orders listed")
            resp['orders'] = orders_info
            return resp, 200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def delete_restaurant_order(res_id: int, order_id: int):
        current_user = get_jwt_identity()

        try:
            if not validate_restaurant(current_user, res_id):
                return validation_error(False, "Unauthorized Access"), 400
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

        if not (order := Order.query.filter_by(order_id=order_id, is_active=True).first()):
            return err_resp(msg="Order not found", code=404, reason="no_order")

        order_info = order_schema.dump(order)
        if order_info["res_id"] != res_id:
            return validation_error(False, "Unauthorized Access"), 400

        try:
            order.is_active = False
            order.status = STATUS.RES_CANCELLED
            db.session.commit()
            resp = message(True, "Order deleted successfully")
            return resp, 200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def get_restaurant_order_detail(res_id: int, order_id: int):
        current_user = get_jwt_identity()

        try:
            if not validate_restaurant(current_user, res_id):
                return validation_error(False, "Unauthorized Access"), 400
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

        if not (order := Order.query.filter_by(order_id=order_id, is_active=True).first()):
            return err_resp(msg="Order not found", code=404, reason="no_order")

        order_info = order_schema.dump(order)
        if order_info["res_id"] != res_id:
            return validation_error(False, "Unauthorized Access"), 400

        order_status = order.get_status().name

        try:
            order_details_obj = OrderDetail.query.filter_by(order_id=order_id)

            order_details_info = [order_detail_schema.dump(order_detail) for order_detail in order_details_obj]

            burgers = []
            for order_detail in order_details_info:
                burger_id = order_detail["burger_id"]
                burger = Burger.query.get(burger_id)
                burger_info = burger_schema.dump(burger)
                quantity = order_detail["quantity"]
                burger_info["quantity"] = quantity
                burgers.append(burger_info)
            resp = message(True, "Order detail listed successfully")
            resp["burgers"] = burgers
            resp["order_status"] = order_status
            return resp, 200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def update_restaurant_order(res_id: int, order_id: int, data: dict):
        current_user = get_jwt_identity()

        try:
            if not validate_restaurant(current_user, res_id):
                return validation_error(False, "Unauthorized Access"), 400
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

        if not (order := Order.query.filter_by(order_id=order_id).first()):
            return err_resp(msg="Order not found", code=404, reason="no_order")

        order_info = order_schema.dump(order)
        if order_info["res_id"] != res_id:
            return validation_error(False, "Unauthorized Access"), 400

        try:
            status_id = data["status_id"]
            if STATUS.PREPARING.value == status_id:
                order.status = STATUS.PREPARING
                order.is_active = True
            elif STATUS.RES_CANCELLED.value == status_id:
                order.status = STATUS.RES_CANCELLED
                order.is_active = False
            elif STATUS.ON_THE_WAY.value == status_id:
                order.status = STATUS.ON_THE_WAY
                order.is_active = True
            elif STATUS.DELIVERED.value == status_id:
                order.status = STATUS.DELIVERED
                order.is_active = False
            elif STATUS.NEW.value == status_id:
                order.status = STATUS.NEW
                order.is_active = True

            db.session.commit()
            resp = message(True, "Order updated successfully")
            return resp, 200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()
