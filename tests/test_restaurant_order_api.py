import json

from flask_jwt_extended import create_access_token

from app import db
from app.models.order import Order
from tests.utils.base import BaseTestCase
from app.models.restaurant import Restaurant


def get_orders(self, res_id, access_token):
    return self.client.get(
        f"/api/restaurant/{res_id}/orders",
        content_type="application/json",
        headers={"Authorization": "Bearer " + access_token}
    )


def get_order_detail(self, res_id, order_id, access_token):
    return self.client.get(
        f"/api/restaurant/{res_id}/order/{order_id}",
        content_type="application/json",
        headers={"Authorization": "Bearer " + access_token}
    )


def delete_order(self, res_id, order_id, access_token):
    return self.client.delete(
        f"/api/restaurant/{res_id}/order/{order_id}",
        content_type="application/json",
        headers={"Authorization": "Bearer " + access_token}
    )


def update_order(self, res_id, order_id, data, access_token):
    return self.client.put(
        f"/api/restaurant/{res_id}/order/{order_id}",
        content_type="application/json",
        data=json.dumps(data),
        headers={"Authorization": "Bearer " + access_token}
    )


def insert_order(user_id, res_id):
    res_name = 'Test Burger'

    db.session.add(
        Restaurant(
            user_id=user_id,
            name=res_name
        )
    )

    db.session.add(
        Order(
            total_price=100,
            res_id=res_id,
            user_id=user_id
        )
    )

    db.session.commit()


class TestRestaurantOrder(BaseTestCase):
    def test_get_order(self):
        """ Test getting order """
        user_id = 1
        res_id = 1
        order_count = 3

        for i in range(order_count):
            insert_order(user_id, res_id)

        diff_user_id = 2
        diff_res_id = 2
        insert_order(diff_user_id, diff_res_id)  # different restaurant order

        identity = dict(
            user_id=user_id,
            is_restaurant=True,
            username='testuser'
        )

        access_token = create_access_token(identity=identity)

        orders_resp = get_orders(self, res_id, access_token)
        order_data = json.loads(orders_resp.data.decode())

        self.assertEquals(orders_resp.status_code, 200)
        self.assertEquals(len(order_data['orders']), order_count)

        for i in range(order_count):
            self.assertEquals(order_data['orders'][i]['res_id'], res_id)

    def test_get_order_detail(self):
        """ test get order detail """
        user_id = 1
        res_id = 1
        order_count = 3

        for i in range(order_count):
            insert_order(user_id, res_id)

        identity = dict(
            user_id=user_id,
            is_restaurant=True,
            username='testuser'
        )

        access_token = create_access_token(identity=identity)

        for i in range(order_count):
            order_resp = get_order_detail(self, res_id, i + 1, access_token)
            self.assertEquals(order_resp.status_code, 200)

    def test_delete_order(self):
        """ Test delete order """
        user_id = 1
        res_id = 1
        order_count = 3

        for i in range(order_count):
            insert_order(user_id, res_id)

        identity = dict(
            user_id=user_id,
            is_restaurant=True,
            username='testuser'
        )

        access_token = create_access_token(identity=identity)

        delete_order_id = 1
        del_resp = delete_order(self, res_id, delete_order_id, access_token)
        self.assertEquals(del_resp.status_code, 200)

        deleted_order = Order.query.filter_by(order_id=delete_order_id, is_active=True).first()
        self.assertIsNone(deleted_order)

        exist_order_id = 2
        order = Order.query.filter_by(order_id=exist_order_id, is_active=True).first()
        self.assertIsNotNone(order)

    def test_update_order(self):
        user_id = 1
        res_id = 1
        order_count = 3

        for i in range(order_count):
            insert_order(user_id, res_id)

        identity = dict(
            user_id=user_id,
            is_restaurant=True,
            username='testuser'
        )

        access_token = create_access_token(identity=identity)

        new_status_id = 2
        payload = dict(
            status_id=new_status_id
        )

        order_id = 1

        update_resp = update_order(self, res_id, order_id, payload, access_token)
        self.assertEquals(update_resp.status_code, 200)

        order = Order.query.get(order_id)
        self.assertEquals(order.get_status().value, new_status_id)
        self.assertFalse(order.is_active)

    def test_update_order_wrong_status_id(self):
        """ Test try tp update with wrong status code """
        user_id = 1
        res_id = 1
        order_count = 3

        for i in range(order_count):
            insert_order(user_id, res_id)

        identity = dict(
            user_id=user_id,
            is_restaurant=True,
            username='testuser'
        )

        access_token = create_access_token(identity=identity)

        new_status_id = 5
        payload = dict(
            status_id=new_status_id
        )

        order_id = 1

        update_resp = update_order(self, res_id, order_id, payload, access_token)
        self.assertEquals(update_resp.status_code, 400)