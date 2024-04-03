from datetime import datetime
from app import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.String(255), nullable=False)
    # user_cart_id = db.Column(db.Integer, db.ForeignKey('user_carts.id'), nullable=False)

    # cart_owner = db.relationship("UserCartModel", back_populates='items')

    def from_dict(self, a_dict):
        self.title = a_dict.get('title')
        self.body = a_dict.get('body')
        # self.user_cart_id = int(a_dict.get('user_cart_id'))

    def save_item(self):
        db.session.add(self)
        db.session.commit()

    def del_item(self):
        db.session.delete(self)
        db.session.commit()
