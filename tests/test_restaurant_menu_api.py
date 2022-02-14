import json

from flask_jwt_extended import create_access_token

from app import db
from app.models.burger import Burger
from tests.utils.base import BaseTestCase
from app.models.restaurant import Restaurant


def get_restaurants(self):
    return self.client.get(
        f"/api/restaurant",
        content_type="application/json",
    )


def get_restaurant_menu(self, res_id):
    return self.client.get(
        f"/api/restaurant/{res_id}/menu",
        content_type="application/json",
    )


def post_restaurant_menu_item(self, res_id, data, access_token):
    return self.client.post(
        f"/api/restaurant/{res_id}/menu",
        data=json.dumps(data),
        content_type="application/json",
        headers={"Authorization": "Bearer " + access_token}
    )


def get_burger_detail(self, res_id, burger_id):
    return self.client.get(
        f"/api/restaurant/{res_id}/menu/{burger_id}",
        content_type="application/json",
    )


def put_burger_detail(self, res_id, burger_id, data, access_token):
    return self.client.put(
        f"/api/restaurant/{res_id}/menu/{burger_id}",
        data=json.dumps(data),
        content_type="application/json",
        headers={"Authorization": "Bearer " + access_token}
    )


def delete_burger(self, res_id, burger_id, access_token):
    return self.client.delete(
        f"/api/restaurant/{res_id}/menu/{burger_id}",
        content_type="application/json",
        headers={"Authorization": "Bearer " + access_token}
    )


def insert_burger(user_id, res_id):
    res_name = 'Test Burger'

    db.session.add(
        Restaurant(
            user_id=user_id,
            name=res_name
        )
    )

    db.session.add(
        Burger(
            name='Enfes Burger',
            price=25,
            description='Test burger',
            image_path='test/path',
            res_id=res_id
        )
    )

    db.session.commit()


class TestRestaurantMenu(BaseTestCase):
    def test_restaurants_get(self):
        """ Test getting a restaurant from DB """

        res_count = 3
        res_name = 'Test Burger'

        for i in range(res_count):
            db.session.add(
                Restaurant(
                    name=f'{res_name} {i}',
                    user_id=i
                )
            )
        db.session.commit()

        res_resp = get_restaurants(self)
        res_data = json.loads(res_resp.data.decode())

        self.assertTrue(res_resp.status)
        self.assertEquals(res_resp.status_code, 200)

        self.assertEquals(res_data['restaurants'][res_count - 1]['name'],
                          f'{res_name} {res_count - 1}')
        self.assertEquals(len(res_data['restaurants']), res_count)

    def test_restaurant_menu_get(self):
        """ Test getting restaurant menu from DB """

        res_id = 1
        res_name = 'Test Burger'

        db.session.add(
            Restaurant(
                name=res_name,
                res_id=res_id,
                user_id=1
            )
        )

        burger_count = 3

        for i in range(burger_count):
            db.session.add(
                Burger(
                    name=f'Burger {i}',
                    price=i * 10,
                    description=f'Delicious Burger {i}',
                    image_path=f'test/path/{i}',
                    res_id=res_id
                )
            )
        db.session.commit()

        menu_resp = get_restaurant_menu(self, res_id)
        menu_data = json.loads(menu_resp.data.decode())

        self.assertTrue(menu_resp.status)
        self.assertEquals(menu_resp.status_code, 200)

        for i in range(burger_count):
            self.assertEquals(menu_data['menu'][i]['name'], f'Burger {i}')
        self.assertEquals(len(menu_data['menu']), burger_count)

    def test_not_exist_res_id(self):
        """ Test Reach not exist restaurant """
        wrong_res_id = 1

        menu_resp = get_restaurant_menu(self, wrong_res_id)

        self.assertEquals(menu_resp.status_code, 404)

    def test_insert_burger(self):
        """ Test insert burger to menu """
        user_id = 1
        db.session.add(
            Restaurant(
                user_id=user_id
            )
        )

        identity = dict(
            is_restaurant=True,
            username='test',
            user_id=user_id
        )

        burger_payload = dict(
            name='Enfes Burger',
            price=25,
            description='Test burger',
            image_path='test/path'
        )

        access_token = create_access_token(identity=identity)

        post_rep = post_restaurant_menu_item(self, 1, burger_payload, access_token)
        self.assertEquals(post_rep.status_code, 200)

    def test_insert_burger_wrong_restaurant(self):
        """ Test insert burger to not you restaurant """

        user_id = 1
        test_user_id = 2

        db.session.add(
            Restaurant(
                user_id=user_id
            )
        )

        db.session.add(
            Restaurant(
                user_id=test_user_id
            )
        )

        wrong_identity = dict(
            is_restaurant=True,
            username='wrongtest',
            user_id=test_user_id
        )

        burger_payload = dict(
            name='Enfes Burger',
            price=25,
            description='Test burger',
            image_path='test/path'
        )

        access_token = create_access_token(identity=wrong_identity)

        post_rep = post_restaurant_menu_item(self, 1, burger_payload, access_token)
        self.assertEquals(post_rep.status_code, 400)

    def test_get_burger_detail(self):
        """ Test for get burger detail """
        user_id = 1
        res_id = 1

        db.session.add(
            Restaurant(
                user_id=user_id
            )
        )

        db.session.add(
            Burger(
                name='Enfes Burger',
                price=25,
                description='Test burger',
                image_path='test/path',
                res_id=res_id
            )
        )

        db.session.commit()

        burger_id = 1

        burger_resp = get_burger_detail(self, res_id, burger_id)
        burger_data = json.loads(burger_resp.data.decode())

        self.assertEquals(burger_resp.status_code, 200)
        self.assertEquals(burger_data['burger']['name'], 'Enfes Burger')
        self.assertEquals(burger_data['burger']['burger_id'], burger_id)

    def test_update_burger(self):
        """ Test update burger """
        user_id = 1
        res_id = 1
        insert_burger(user_id, res_id)

        update_name = 'Leziz Burger'
        update_desc = 'Leziz Burger desc'

        burger_update_payload = dict(
            name=update_name,
            price=25,
            description=update_desc,
            image_path='test/path',
            is_active=True
        )

        identity = dict(
            username='testuser',
            user_id=user_id,
            is_restaurant=True
        )

        access_token = create_access_token(identity=identity)

        update_resp = put_burger_detail(self, res_id, 1, burger_update_payload, access_token)
        self.assertEquals(update_resp.status_code, 200)

        burger_resp = get_burger_detail(self, res_id, 1)
        burger_data = json.loads(burger_resp.data.decode())
        self.assertEquals(burger_data['burger']['name'], update_name)
        self.assertEquals(burger_data['burger']['description'], update_desc)

        wrong_identity = dict(
            username='randomuser',
            user_id=2,
            is_restaurant=True
        )

        rnd_access_token = create_access_token(identity=wrong_identity)
        wrong_resp = put_burger_detail(self, res_id, 1, burger_update_payload, rnd_access_token)
        self.assertEquals(wrong_resp.status_code, 400)

    def test_update_burger_missing_field(self):
        """ Test update burger with missing field """
        user_id = 1
        res_id = 1

        insert_burger(user_id, res_id)

        update_name = 'Leziz Burger'
        update_desc = 'Leziz Burger desc'

        burger_update_payload = dict(
            name=update_name,
            price=25,
            description=update_desc,
            is_active=True
            # missing image_path
        )

        identity = dict(
            username='testuser',
            user_id=user_id,
            is_restaurant=True
        )

        access_token = create_access_token(identity=identity)

        update_resp = put_burger_detail(self, res_id, 1, burger_update_payload, access_token)
        self.assertEquals(update_resp.status_code, 400)

    def test_delete_burger(self):
        """ Test delete burger """
        user_id = 1
        res_id = 1

        insert_burger(user_id, res_id)

        identity = dict(
            username='testuser',
            user_id=user_id,
            is_restaurant=True
        )

        access_token = create_access_token(identity=identity)

        delete_resp = delete_burger(self, res_id, 1, access_token)
        self.assertEquals(delete_resp.status_code, 200)

        burger = Burger.query.filter_by(burger_id=1, is_active=True).first()
        self.assertIsNone(burger)
