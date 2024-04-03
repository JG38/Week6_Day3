from flask.views import MethodView
from flask_smorest import abort
from . import bp
from schemas import ItemSchema
from models.item_model import ItemModel

@bp.route('/item', methods=['POST'])
class ItemList(MethodView):

    @bp.arguments(ItemSchema)
    @bp.response(201, ItemSchema)
    def post(self, item_data):
        try:
            item = ItemModel()
            item.from_dict(item_data)
            item.save_item()
            return item
        except Exception as e:
            abort(400, message="Failed to post item")

    @bp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

@bp.route('/item/<item_id>', methods=['GET', 'PUT', 'DELETE'])
class Item(MethodView):

    @bp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return ItemModel.query.get(item_id)
        except Exception as e:
            abort(400, message="Item not found")

    @bp.arguments(ItemSchema)
    @bp.response(201, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if not item:
            abort(400, message="Item not found")
        item.from_dict(item_data)
        item.save_item()
        return item

    def delete(self, item_id):
        item = ItemModel.query.get(item_id)
        if not item:
            abort(400, message="Item not found")
        item.del_item()
        return {'message': f'Item {item_id} deleted'}, 200
