import logging
import secrets
from base64 import b64decode
from datetime import timedelta

from app.extensions import db
from app.models import UserAdmin
from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash, generate_password_hash


class Login(Resource):
    def get(self):
        if not request.headers.get("Authorization"):
            return {"error": "login e senha inválidos."}, 400
        basic, code = request.headers["Authorization"].split(" ")
        if not basic.lower() == "basic":
            return {"error": "Authorization mal formatado!"}, 400

        email, password = b64decode(code).decode().split(":")

        user = UserAdmin.query.filter_by(email=email).first()
        if not user or check_password_hash(user.password, password):
            return {"error": "login e senha inválidos."}, 400

        # Criação de token temporária, depois necessita
        # passar um subtoken para diversificar o admin do
        # cliente padrão.
        token = create_access_token(
            {"id": user.id}, expires_delta=timedelta(minutes=30)
        )

        return {"success": token}, 201
