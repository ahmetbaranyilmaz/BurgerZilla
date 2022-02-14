from app import db


class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    res_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    is_active = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), index=True)

    res_burger = db.relationship("Burger", backref="restaurant", lazy="dynamic")
    res_order = db.relationship("Order", backref="restaurant", lazy="dynamic")

    def __repr__(self):
        return '<Restaurant {}>'.format(self.name)

    def get_name(self):
        return self.name

    def get_user_id(self):
        return self.user_id

    @staticmethod
    def insert_restaurant():
        omer = Restaurant(
            name='Dombili Burger',
            user_id=3
        )
        db.session.add(omer)

        tunc = Restaurant(
            name='Dublemumble',
            user_id=4
        )
        db.session.add(tunc)

        db.session.commit()
