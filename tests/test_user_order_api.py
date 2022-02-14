import json
from flask_jwt_extended import create_access_token
from app import db
from app.models.order import Order
from tests.utils.base import BaseTestCase
from app.models.restaurant import Restaurant
from app.models.burger import Burger
from app.models.order_detail import OrderDetail
from app.models.user import User


def get_orders(self, username, access_token):
    return self.client.get(
        f"/api/{username}/orders",
        content_type="application/json",
        headers={"Authorization": "Bearer " + access_token}
    )


def post_order(self, username, data, access_token):
    return self.client.post(
        f"/api/{username}/orders",
        content_type="application/json",
        data=json.dumps(data),
        headers={"Authorization": "Bearer " + access_token}
    )


def get_order_detail(self, username, order_id, access_token):
    return self.client.get(
        f"/api/{username}/order/{order_id}",
        content_type="application/json",
        headers={"Authorization": "Bearer " + access_token}
    )


def update_order(self, username, order_id, data, access_token):
    return self.client.put(
        f"/api/{username}/order/{order_id}",
        content_type="application/json",
        data=json.dumps(data),
        headers={"Authorization": "Bearer " + access_token}
    )


def delete_order(self, username, order_id, access_token):
    return self.client.delete(
        f"/api/{username}/order/{order_id}",
        content_type="application/json",
        headers={"Authorization": "Bearer " + access_token}
    )


def insert_order(user_id, res_id=1):
    db.session.add(
        Order(
            total_price=100,
            res_id=res_id,
            user_id=user_id
        )
    )

    db.session.commit()


def insert_order_detail(user_id=1, username='testuser', order_id=1,
                        burger_price=20, quantity=1):
    db.session.add(
        User(
            user_id=user_id,
            username=username
        )
    )

    res_user_id = 2
    res_username = 'testres'

    db.session.add(
        User(
            user_id=res_user_id,
            username=res_username,
            is_restaurant=True
        )
    )

    res_id = 1
    res_name = 'Test Burger'

    db.session.add(
        Restaurant(
            res_id=res_id,
            name=res_name,
            user_id=user_id
        )
    )

    burger_id = 1
    burger_name = 'Test Hamburger'

    db.session.add(
        Burger(
            burger_id=burger_id,
            name=burger_name,
            res_id=res_id,
            price=burger_price
        )
    )

    db.session.add(
        Order(
            order_id=order_id,
            total_price=burger_price * quantity,
            user_id=user_id,
            res_id=res_id
        )
    )

    db.session.add(
        OrderDetail(
            quantity=quantity,
            burger_id=burger_id,
            order_id=order_id
        )
    )

    db.session.commit()


class TestRestaurantOrder(BaseTestCase):
    def test_get_user_order(self):
        """ test get user order """
        user_id = 1
        res_id = 2
        username = 'testuser'
        name = 'Test User'

        db.session.add(
            User(
                user_id=user_id,
                name=name,
                username=username
            )
        )

        db.session.add(
            Restaurant(
                name='Test Burger',
                res_id=res_id
            )
        )

        db.session.commit()

        order_count = 3

        for i in range(order_count):
            insert_order(user_id, res_id)

        identity = dict(
            user_id=user_id,
            username=username,
            is_restaurant=False
        )

        access_token = create_access_token(identity=identity)

        order_resp = get_orders(self, username, access_token)
        order_data = json.loads(order_resp.data.decode())
        self.assertEquals(order_resp.status_code, 200)
        for order in order_data['orders']:
            self.assertEquals(order['res_id'], res_id)
            self.assertEquals(order['user_id'], user_id)

    def test_insert_order(self):
        """ test insert order """
        user_id = 1
        res_id = 2
        username = 'testuser'
        name = 'Test User'

        db.session.add(
            User(
                user_id=user_id,
                name=name,
                username=username
            )
        )

        db.session.add(
            Restaurant(
                name='Test Burger',
                res_id=res_id
            )
        )

        burger_price = 20
        db.session.add(
            Burger(
                name='Leziz Burger',
                price=burger_price,
                res_id=res_id
            )
        )

        db.session.commit()

        burger_quantity = 2
        payload = dict(
            burgers=[
                dict(
                    burger_id=1,
                    quantity=burger_quantity
                )
            ]
        )

        identity = dict(
            user_id=user_id,
            username=username,
            is_restaurant=False
        )

        access_token = create_access_token(identity=identity)

        post_resp = post_order(self, username, payload, access_token)
        self.assertEquals(post_resp.status_code, 200)

        order = Order.query.get(1)
        self.assertEquals(order.user_id, user_id)
        self.assertEquals(order.total_price, burger_price * burger_quantity)

    def test_get_order_detail(self):
        """ Test getting order detail """
        user_id = 1
        username = 'testuser'

        order_id = 1
        burger_price = 20
        quantity = 2
        insert_order_detail(user_id, username, order_id, burger_price, quantity)

        identity = dict(
            user_id=user_id,
            username=username,
            is_restaurant=False
        )

        access_token = create_access_token(identity=identity)

        detail_resp = get_order_detail(self, username, order_id, access_token)
        self.assertEquals(detail_resp.status_code, 200)

        detail_data = json.loads(detail_resp.data.decode())
        self.assertEquals(detail_data['order']['total_price'], burger_price * quantity)

    def test_update_order(self):
        """ Test for updating order with new quantity """
        user_id = 1
        username = 'testuser'

        order_id = 1
        burger_price = 20
        quantity = 1
        insert_order_detail(user_id, username, order_id, burger_price, quantity)

        identity = dict(
            user_id=user_id,
            username=username,
            is_restaurant=False
        )

        new_quantity = 5
        payload = dict(
            burger_id=1,
            quantity=new_quantity
        )

        access_token = create_access_token(identity=identity)

        update_resp = update_order(self, username, order_id, payload, access_token)
        self.assertEquals(update_resp.status_code, 200)

        order_detail = OrderDetail.query.get(1)
        self.assertEquals(order_detail.quantity, new_quantity)

        order = Order.query.get(order_id)
        self.assertEquals(order.total_price, new_quantity * burger_price)

    def test_cancel_order(self):
        user_id = 1
        username = 'testuser'

        order_id = 1
        insert_order_detail(user_id, username, order_id)

        identity = dict(
            user_id=user_id,
            username=username,
            is_restaurant=False
        )

        access_token = create_access_token(identity=identity)
        delete_resp = delete_order(self, username, order_id, access_token)
        self.assertEquals(delete_resp.status_code, 200)

        order = Order.query.filter_by(order_id=order_id, is_active=True).first()

        self.assertIsNone(order)
