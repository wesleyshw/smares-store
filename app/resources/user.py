from flask_jwt_extended import current_user
from flask_restful import Resource, marshal
from app.models import User
from app.services.auth import auth
from app.schemas import user_items_fields


class Orders(Resource):
    @auth()
    def get(self):
        if not current_user:
            return {"error": "Acesso negado, faça o login."}, 400
        return marshal(current_user.items, user_items_fields, "orders")
