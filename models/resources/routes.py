from flask.views import MethodView
from flask_smorest import abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user_cart_model import UserCartModel
from app.models.grab_item_model import GrabItemModel
from app.models.item_model import ItemModel
from app.schemas import ItemSchema, UserCartSchema, GrabbedItemWithUserCartSchema
from app import bp

@bp.route('/grab-item/<item_id>', methods=['POST'])
class GrabItem(MethodView):

    @jwt_required()
    @bp.response(201, ItemSchema)
    def post(self, item_id):
        user_cart_id = get_jwt_identity()
        item = ItemModel.query.get(item_id)
        user_cart = UserCartModel.query.get(user_cart_id)
        
        if user_cart and item:
            grabbed_by_user_cart = GrabItemModel.query.filter_by(item_id=item_id, user_cart_id=user_cart_id).all()
            
            if grabbed_by_user_cart:
                return item
            
            grab_item = GrabItemModel(user_cart_id=user_cart_id, item_id=item_id)
            grab_item.save()
            
            return item
        
        abort(400, message="Invalid Item")
