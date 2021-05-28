from . import api
from app import db, models


@api.route("/index")
def index():

    return "index"
