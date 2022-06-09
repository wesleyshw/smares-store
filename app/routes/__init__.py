from app.routes.resources import admin, users
from flask_restful import Api
from flask import Blueprint


bp = Blueprint("api", __name__, url_prefix="/api/v1")
bp_admin = Blueprint("api_admin", __name__, url_prefix="/admin")
bp_users = Blueprint("api_users", __name__, url_prefix="/users")

api_admin = Api(bp_admin)
api_users = Api(bp_users)


def init_app(app):

    bp.register_blueprint(bp_users)
    bp.register_blueprint(bp_admin)
    admin.init_api(api_admin)
    users.init_api(api_users)
    app.register_blueprint(bp)
