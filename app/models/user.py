from datetime import datetime
from app import db, bcrypt


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(15), unique=True)
    name = db.Column(db.String(64))
    is_active = db.Column(db.Boolean, default=True)
    password_hash = db.Column(db.String(128))
    joined_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_restaurant = db.Column(db.Boolean, default=False)

    user_restaurant = db.relationship("Restaurant", backref="user", lazy="dynamic")
    user_order = db.relationship("Order", backref="user", lazy="dynamic")

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

    @staticmethod
    def insert_user():
        ugur = User(
            name='Uğur Özyalı',
            username='ugur',
            email='ugurozy@musteri.nett',
            password='testpass'
        )
        db.session.add(ugur)

        ezel = User(
            name='Ezel Özlüyalı',
            username='ezel',
            email='ezelozy@musteri.nett',
            password='testpass'
        )
        db.session.add(ezel)

        omer = User(
            name='Ömer Kandor',
            username='omer',
            email='omer@musteri.nett',
            password='testpass',
            is_restaurant=True
        )
        db.session.add(omer)

        tunc = User(
            name='Tunç Dimdal',
            username='tunc',
            email='tunc@musteri.nett',
            password='testpass',
            is_restaurant=True
        )
        db.session.add(tunc)
        db.session.commit()
