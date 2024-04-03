from app import db

class GrabItemModel(db.Model):
    __tablename__ = 'grab_item'

    id = db.Column(db.Integer, primary_key=True)
    user_cart_id = db.Column(db.Integer, db.ForeignKey('user_carts.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)

    cart_owner = db.relationship("UserCartModel", back_populates='grabbed_items')

    def save(self):
        with db.session.begin():
            db.session.add(self)

    def delete(self):
        with db.session.begin():
            db.session.delete(self)
