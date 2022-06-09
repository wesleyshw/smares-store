from flask_jwt_extended import current_user
from flask_restful import Resource, marshal, reqparse
from app.models import User, Profile
from app.services.auth import jwt_auth
from app.schemas import user_items_fields


class Profile(Resource):
    @jwt_auth()
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "first_name",
            required=True,
            help="o campo first_name é obrigatório",
        )
        parser.add_argument(
            "last_name", required=True, help="o campo last_name é obrigatório"
        )
        parser.add_argument(
            "last_name", required=True, help="o campo last_name é obrigatório"
        )
        parser.add_argument(
            "last_name", required=True, help="o campo last_name é obrigatório"
        )
        parser.add_argument(
            "last_name", required=True, help="o campo last_name é obrigatório"
        )
        args = parser.parse_args()
        if not current_user:
            return {"error": "Acesso negado. faça o login."}, 400
        if not current_user.profile:
            current_user.profile = Profile()


class Orders(Resource):
    @jwt_auth()
    def get(self):
        if not current_user:
            return {"error": "Acesso negado, faça o login."}, 400
        return marshal(current_user.items, user_items_fields, "orders")
