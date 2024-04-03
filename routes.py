from flask import request, jsonify
from flask.views import MethodView
from uuid import uuid4
from flask_smorest import abort
from flask_jwt_extended import create_access_token, unset_jwt_cookies
from schemas import UserCartSchema, UserCartWithGrabbedItemsSchema, GrabbedItemWithUserCartSchema
from . import bp
from models.user_cart_model import UserCartModel

@bp.route('/user_cart', methods=['GET', 'POST'])
class UserCartList(MethodView):

    @bp.response(200, UserCartWithGrabbedItemsSchema(many=True))
    def get(self):
        user_carts = UserCartModel.query.all()
        return user_carts

    @bp.arguments(UserCartSchema)
    @bp.response(201, UserCartSchema)
    def post(self, data):
        try:
            user_cart = UserCartModel()
            user_cart.from_dict(data)
            user_cart.save_user_cart()
            return user_cart, 201
        except:
            abort(400, message="Username already taken, please try a different one!")


@bp.route('/user_cart/<int:id>', methods=['GET', 'PUT', 'DELETE'])
class UserCart(MethodView):

    @bp.response(200, UserCartWithGrabbedItemsSchema)
    def get(self, id):
        user_cart = UserCartModel.query.get(id)
        if user_cart:
            return user_cart
        else:
            abort(400, message="Not a valid user cart")

    @bp.arguments(UserCartSchema)
    @bp.response(200, UserCartWithGrabbedItemsSchema)
    def put(self, data, id):
        user_cart = UserCartModel.query.get(id)
        if user_cart:
            user_cart.from_dict(data)
            user_cart.save_user_cart()
            return user_cart
        else:
            abort(400, message="Not a valid user cart")

    def delete(self, id):
        user_cart = UserCartModel.query.get(id)
        if user_cart:
            user_cart.del_user_cart()
            return {"message": "User cart GONE GONE"}, 200
        abort(400, message="Not a valid user cart")


@bp.post('/login')
def login():
    login_data = request.get_json()
    username = login_data['username']

    user_cart = UserCartModel.query.filter_by(username=username).first()
    if user_cart and user_cart.check_password(login_data['password']):
        access_token = create_access_token(identity=user_cart.id)
        return {'access_token': access_token}, 201

    abort(400, message="Invalid User Data")


@bp.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "Logout successful"})
    unset_jwt_cookies(response)
    return response
