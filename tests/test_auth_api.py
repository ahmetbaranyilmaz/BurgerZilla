import json

from tests.utils.base import BaseTestCase
from tests.utils.common import register_user, login_user, register_restaurant


class TestAuthBlueprint(BaseTestCase):
    def test_register_login(self):
        """ Test Auth API registration and login """
        data = dict(
            email="test@user.com",
            username="test.User",
            name="Test User",
            password="test1234",
        )

        register_resp = register_user(self, data)
        register_data = json.loads(register_resp.data.decode())

        self.assertEquals(register_resp.status_code, 200)
        self.assertTrue(register_resp.status)
        self.assertEquals(register_data["user"]["username"], data["username"])

        login_resp = login_user(self, data["email"], data["password"])
        login_data = json.loads(login_resp.data.decode())

        self.assertEquals(login_resp.status_code, 200)
        self.assertTrue(login_resp.status)
        self.assertEquals(login_data["user"]["email"], data["email"])
        self.assertFalse(login_data['user']['is_restaurant'])

    def test_restaurant_register_login(self):
        """
        Test Restaurant register and login
        :return:
        """
        data = dict(
            email="test@burger.com",
            username="burger",
            name="Test Burger",
            password="test1234",
        )

        register_user(self, data)

        login_resp = login_user(self, data["email"], data["password"])
        login_data = json.loads(login_resp.data.decode())

        self.assertFalse(login_data['user']['is_restaurant'])

        register_payload = dict(
            name="Burger King"
        )

        access_token = "randomtoken"
        register_resp = register_restaurant(self, register_payload, access_token)
        self.assertEquals(register_resp.status_code, 422)

        access_token = login_data["access_token"]
        register_resp = register_restaurant(self, register_payload, access_token)
        register_data = json.loads(register_resp.data.decode())

        self.assertEquals(register_resp.status_code, 200)
        self.assertEquals(register_data["user"]["name"], register_payload["name"])

        login_resp = login_user(self, data["email"], data["password"])
        login_data = json.loads(login_resp.data.decode())

        self.assertTrue(login_data['user']['is_restaurant'])

    def test_register_with_same_mail(self):
        """
        Test Registering with exist email
        """
        data = dict(
            email="test@user.com",
            username="test.User",
            name="Test User",
            password="test1234",
        )
        register_user(self, data)

        same_mail = dict(
            email="test@user.com",
            username="notsame",
            name="Not same",
            password="notsamepass"
        )

        register_resp = register_user(self, same_mail)

        self.assertEquals(register_resp.status_code, 409)

    def test_register_with_same_username(self):
        """
        Test Register with exist username
        """
        data = dict(
            email="test@user.com",
            username="test.User",
            name="Test User",
            password="test1234",
        )
        register_user(self, data)

        same_mail = dict(
            email="notsame@user.com",
            username="test.User",
            name="Not same",
            password="notsamepass"
        )

        register_resp = register_user(self, same_mail)

        self.assertEquals(register_resp.status_code, 409)

    def test_register_with_same_name(self):
        """
        Test Register with exist Name
        """
        data = dict(
            email="test@user.com",
            username="test.User",
            name="Test User",
            password="test1234",
        )
        register_user(self, data)

        same_mail = dict(
            email="notsame@user.com",
            username="notsame",
            name="Test User",
            password="notsamepass"
        )

        register_resp = register_user(self, same_mail)

        self.assertEquals(register_resp.status_code, 200)
