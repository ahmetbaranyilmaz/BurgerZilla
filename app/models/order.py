from datetime import datetime
from app import db
from app.constants.status import STATUS


class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum(STATUS), default=STATUS.NEW)
    total_price = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), index=True)
    res_id = db.Column(db.Integer, db.ForeignKey('restaurants.res_id'), index=True)

    order_detail = db.relationship("OrderDetail", backref="order", lazy="dynamic")

    def __repr__(self):
        return '<Order {}>'.format(self.order_id)

    def get_status(self):
        return self.status
