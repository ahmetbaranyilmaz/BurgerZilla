from app import ma
from .user import User
from .order import Order
from .burger import Burger
from .order_detail import OrderDetail
from .restaurant import Restaurant


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("email", "username", "name", "joined_date", "is_restaurant", "is_active")


class RestaurantSchema(ma.Schema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("name", "user_id", "is_active", "res_id")


class BurgerSchema(ma.Schema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("name", "price", "description", "image_path", "res_id", "is_active", "burger_id")


class OrderSchema(ma.Schema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("order_id", "order_date", "total_price", "user_id", "res_id", "is_active")


class OrderDetailSchema(ma.Schema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("burger_id", "order_id", "quantity")
