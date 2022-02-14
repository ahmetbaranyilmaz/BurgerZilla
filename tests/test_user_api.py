import json
from flask_jwt_extended import create_access_token
from app import db
from app.models.user import User
from tests.utils.base import BaseTestCase


def get_user_data(self, access_token, username):
    return self.client.get(
        f"/api/{username}",
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )


class TestUserBlueprint(BaseTestCase):
    def test_user_get(self):
        """ Test getting a user from DB """

        # Create a mock user
        username = 'testuser'
        user = User(
            username=username,
            email='testuser@test.com',
            name='Test User'
        )

        db.session.add(user)
        db.session.commit()

        user = User.query.filter_by(username=username).first()

        identity = dict(
            user_id=user.user_id,
            is_restaurant=user.is_restaurant,
            username=user.username
        )

        access_token = create_access_token(identity=identity)
        user_resp = get_user_data(self, access_token, username)
        user_data = json.loads(user_resp.data.decode())

        self.assertTrue(user_resp.status)
        self.assertEquals(user_resp.status_code, 200)
        self.assertEquals(user_data['user']['username'], username)

        wrong_identity = dict(
            user_id=2,
            is_restaurant=False,
            username='random'
        )

        wrong_access_token = create_access_token(identity=wrong_identity)

        unauth_resp = get_user_data(self, wrong_access_token, username)
        self.assertEquals(unauth_resp.status_code, 400)
