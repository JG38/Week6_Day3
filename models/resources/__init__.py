from flask_smorest import Blueprint
from . import routes

bp = Blueprint("grab_item", __name__, description="Routes for Grab Items")

