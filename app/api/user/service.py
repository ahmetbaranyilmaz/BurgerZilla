from flask import current_app
from flask_jwt_extended import get_jwt_identity
from app.utils import err_resp, internal_err_resp, message, validation_error
from .utils import validate_username
from app.models.user import User
from app.models.order import Order
from app.models.burger import Burger
from app.models.restaurant import Restaurant
from app.models.order_detail import OrderDetail
from app import db
from app.constants.status import STATUS
from app.models.schemas import BurgerSchema, OrderSchema, OrderDetailSchema, UserSchema

user_schema = UserSchema()
order_schema = OrderSchema()
burger_schema = BurgerSchema()
order_detail_schema = OrderDetailSchema()


class UserService:
    @staticmethod
    def get_user_data(username: str):
        """
        get user data
        """

        current_user = get_jwt_identity()

        if not validate_username(username, current_user["username"]):
            return validation_error(False, "Unauthorized Access"), 400

        if not (user := User.query.filter_by(username=username).first()):
            return err_resp("User Not Found", "user_404", 404)

        try:
            user_data = user_schema.dump(user)
            resp = message(True, "User data sent")
            resp["user"] = user_data
            return resp, 200
        except Exception as e:
            print("Error User:", e)
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def get_user_orders(username: str):
        """
        Get all orders of a specific user
        """

        current_user = get_jwt_identity()
        user_id = current_user["user_id"]

        if not validate_username(username, current_user["username"]):
            return validation_error(False, "Unauthorized Access"), 400

        if not (Order.query.filter_by(user_id=user_id, is_active=True).first()):
            return err_resp(msg="Orders not found", code=404, reason="no_orders")

        orders = Order.query.filter_by(user_id=user_id, is_active=True)

        try:
            orders_data = []

            for order in orders:
                order_info = order_schema.dump(order)
                order_info["status"] = order.get_status().name
                res_id = order_info["res_id"]
                res_name = Restaurant.query.get(res_id)
                order_info["name"] = res_name.name
                orders_data.append(order_info)

            resp = message(True, "Orders loaded successfully")
            resp["orders"] = orders_data
            return resp, 200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def insert_user_order(username: str, data: dict):
        """
        Insert order of a specific user
        """

        current_user = get_jwt_identity()
        user_id = current_user["user_id"]
        if not validate_username(username, current_user["username"]):
            return validation_error(False, "Unauthorized Access"), 400

        total_price = 0
        res_id = None
        order_details = []
        for order in data["burgers"]:
            burger_id = order["burger_id"]
            burger = Burger.query.filter_by(burger_id=burger_id).first()
            burger_info = burger_schema.dump(burger)
            if not burger_info['is_active']:
                return err_resp(msg="This burger is not active", code=404, reason='no_burger')
            total_price += burger_info["price"] * order["quantity"]
            res_id = burger_info["res_id"]
            order_detail = OrderDetail(
                burger_id=burger_id,
                quantity=order["quantity"]
            )
            order_details.append(order_detail)

        try:
            order = Order(
                user_id=user_id,
                res_id=res_id,
                total_price=total_price
            )
            db.session.add(order)
            db.session.commit()

            for order_detail in order_details:
                order_detail.order_id = order.order_id
                db.session.add(order_detail)

            db.session.commit()

            return message(True, "order created successfully"), 200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def get_user_order_detail(username: str, order_id: int):
        """
        Get all orders detail of a specific user
        """

        current_user = get_jwt_identity()
        user_id = current_user["user_id"]
        if not validate_username(username, current_user["username"]):
            return validation_error(False, "Unauthorized Access"), 400

        if not (order := Order.query.filter_by(user_id=user_id, order_id=order_id, is_active=True).first()):
            return err_resp(msg="Orders not found", code=404, reason="no_orders")

        res_id = order_schema.dump(order)["res_id"]
        res_name = Restaurant.query.filter_by(res_id=res_id).first().get_name()
        order_details = OrderDetail.query.filter_by(order_id=order_id)
        burgers = []
        for order_detail in order_details:
            order_detail_info = order_detail_schema.dump(order_detail)
            burger_id = order_detail_info["burger_id"]
            quantity = order_detail_info["quantity"]

            burger = Burger.query.filter_by(burger_id=burger_id).first()
            burger_info = burger_schema.dump(burger)
            burger_info["quantity"] = quantity
            burgers.append(burger_info)

        try:
            order_info = order_schema.dump(order)
            order_info["res_name"] = res_name
            order_info["status"] = order.get_status().name
            order_info["burgers"] = burgers

            resp = message(True, "Orders loaded successfully")
            resp["order"] = order_info
            return resp, 200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def delete_order(username: str, order_id: int):
        """
        Delete a order by id
        """

        current_user = get_jwt_identity()
        if not validate_username(username, current_user["username"]):
            return validation_error(False, "Unauthorized Access"), 400

        if not (order := Order.query.get(order_id)):
            return err_resp(msg="Order not found", code=404, reason="no_orders")
        try:
            order.is_active = False
            order.status = STATUS.CUSTOMER_CANCELLED
            db.session.commit()
            return message(True, "Order deleted successfully"), 200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def update_order(username: str, order_id: int, data: dict):
        """
        update a order
        """

        current_user = get_jwt_identity()
        if not validate_username(username, current_user["username"]):
            return validation_error(False, "Unauthorized Access"), 400

        burger_id = data["burger_id"]
        quantity = data["quantity"]
        if not (order := Order.query.get(order_id)):
            return err_resp(msg="Order not found", code=404, reason="no_orders")
        try:
            order_detail = OrderDetail.query.filter_by(order_id=order_id, burger_id=burger_id).first()
            order_detail_info = order_detail_schema.dump(order_detail)
            old_quantity = order_detail_info["quantity"]
            order_detail.quantity = quantity
            db.session.commit()

            burger = Burger.query.get(burger_id)
            burger_price = burger.get_price()

            if old_quantity > quantity:
                order.total_price -= (old_quantity-quantity) * burger_price
                db.session.commit()
            else:
                order.total_price += (quantity-old_quantity) * burger_price
                db.session.commit()

            return message(True, "Order updated successfully"), 200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()
