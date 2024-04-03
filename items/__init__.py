from flask_smorest import Blueprint
from .routes import *

bp = Blueprint("items", __name__, description="Routes for Items")

