from app_init import db

class Order(db.Model):
    """
    Order model in the database
    """
    id = db.Column(db.Integer, primary_key = True)
    order_id = db.Column(db.Integer, unique = True, nullable = False)
    price_dollars = db.Column(db.Float, unique = False, nullable = False)
    price_rubles = db.Column(db.Float, unique = False, nullable = False)
    delivery_time = db.Column(db.Date, unique = False, nullable = False)
    notification_is_send = db.Column(db.Boolean, unique = False, default = False)

    def __repr__(self):
        return f"Order:\nID - {self.id}\nOrder ID - {self.order_id}\nPrice dollars - {round(self.price_dollars, 2)}\n" \
               f"Price rubles - {round(self.price_rubles, 2)}\nDelivery time - {self.delivery_time}"


    def to_array(self):
        return [
            self.id, self.order_id, round(self.price_dollars, 2), round(self.price_rubles, 2), self.delivery_time.strftime("%d-%m-%Y")
        ]