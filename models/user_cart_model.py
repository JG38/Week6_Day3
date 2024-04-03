from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class UserCartModel(db.Model):
    __tablename__ = 'user_carts'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    
    grabbed_items = db.relationship("GrabItemModel", back_populates="cart_owner", lazy='dynamic')

    def save_user_cart(self):
        db.session.add(self)
        db.session.commit()

    def del_user_cart(self):
        db.session.delete(self)
        db.session.commit()

    def from_dict(self, user_dict):
        for k, v in user_dict.items():
            if k != 'password':
                setattr(self, k, v)
            else:
                setattr(self, 'password_hash', generate_password_hash(v))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
