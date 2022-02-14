from app import db


class Burger(db.Model):
    __tablename__ = 'burgers'
    burger_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    price = db.Column(db.Integer)
    description = db.Column(db.String(256))
    image_path = db.Column(db.String(256))
    is_active = db.Column(db.Boolean, default=True)
    res_id = db.Column(db.Integer, db.ForeignKey('restaurants.res_id'), index=True)

    burger_order_detail = db.relationship("OrderDetail", backref="burger", lazy="dynamic")

    def __repr__(self):
        return '<Burger {}>'.format(self.name)

    def get_price(self):
        return self.price

    @staticmethod
    def insert_burger():
        bombili = Burger(
            name='Dombili Burger',
            price=30,
            description='Meşhur dombili burger, özel soslu, sarmısaklı ve soğanlı',
            image_path='/dombili/bombili',
            res_id=1
        )
        db.session.add(bombili)

        duble_peynirli = Burger(
            name='Duble Peynirli',
            price=50,
            description='Çift katlı, mozerella ve çedarla bezenmiş dombili burger',
            image_path='/dombili/duble_peynirli',
            res_id=1
        )
        db.session.add(duble_peynirli)

        ac_doyuran = Burger(
            name='Aç Doyuran',
            price=75,
            description='Üç katlı, zeytin soslu, özel ketçap ve tatlı mayonezli burger ve patates',
            image_path='/dombili/ac_doyuran',
            res_id=1
        )
        db.session.add(ac_doyuran)

        tekkatli = Burger(
            name='Tekkatlı',
            price=25,
            description='Bol domatesli, özel muble soslu',
            image_path='/dombili/tekkatli',
            res_id=2
        )
        db.session.add(tekkatli)

        dublemumle = Burger(
            name='Dublemuble',
            price=45,
            description='Çift katlı, beyaz peynir + kaşar peynir soslu, duble hamburger',
            image_path='/dombili/dublemumle',
            res_id=2
        )
        db.session.add(dublemumle)

        deluks = Burger(
            name='Delüks',
            price=70,
            description='Özel dublemuble burger, patates ve eritme peynirle birlikte',
            image_path='/dombili/deluks',
            res_id=2
        )
        db.session.add(deluks)

        db.session.commit()
