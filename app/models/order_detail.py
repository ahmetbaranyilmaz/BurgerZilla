from app import db


class OrderDetail(db.Model):
    __tablename__ = 'order_details'
    order_detail_id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)

    burger_id = db.Column(db.Integer, db.ForeignKey('burgers.burger_id'), index=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), index=True)

    def __repr__(self):
        return '<Order Detail {}>'.format(self.order_detail_id)
