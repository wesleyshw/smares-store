import logging
from app.extensions import db
from app.models import Profile, User
from app.schemas import user_items_fields, profile_fields
from app.services.all.auth import jwt_auth
from flask_jwt_extended import current_user
from flask_restful import Resource, marshal, reqparse


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
            "cpf", required=True, help="o campo cpf é obrigatório"
        )
        parser.add_argument(
            "phone", required=True, help="o campo phone é obrigatório"
        )
        args = parser.parse_args()
        if not current_user:
            return {"error": "Acesso negado. faça o login."}, 400
        if not current_user.profile:
            current_user.profile = Profile()

        current_user.profile.first_name = args.first_name
        current_user.profile.last_name = args.last_name
        current_user.profile.cpf = args.cpf
        current_user.profile.phone = args.phone

        try:
            db.session.commit()
            return marshal(current_user.profile, profile_fields, "profile")
        except Exception as e:
            logging.critical(str(e))
            db.session.rollback()
            return {"error": "Não foi possível preencher o perfil."}, 500


class Orders(Resource):
    @jwt_auth()
    def get(self):
        if not current_user:
            return {"error": "Acesso negado, faça o login."}, 400
        return marshal(current_user.items, user_items_fields, "orders")
