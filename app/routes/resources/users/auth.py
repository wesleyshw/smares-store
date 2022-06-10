import logging
import secrets
from base64 import b64decode
from datetime import timedelta

from app.extensions import db
from app.models import User
from app.services.all.mail import send_mail
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

        user = User.query.filter_by(email=email).first()
        if not user or check_password_hash(user.password, password):
            return {"error": "login e senha inválidos."}, 400

        token = create_access_token(
            {"id": user.id}, expires_delta=timedelta(minutes=30)
        )

        return {"success": token}, 201


class Register(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", required=True, help="o campo email é obrigatório")
        parser.add_argument(
            "password", required=True, help="o campo password é obrigatório"
        )
        args = parser.parse_args()
        user = User.query.filter_by(email=args.email).first()
        if user:
            return {"error": "e-mail já registrado."}, 400

        user = User()
        user.email = args.email
        user.password = generate_password_hash(args.password, salt_length=10)
        db.session.add(user)

        try:
            db.session.commit()
            send_mail(
                "Bem vindo(a) à Smares Store",
                user.email,
                "welcome",
                email=user.email,
            )
            return {"success": "usuário registrado com sucesso."}, 201
        except Exception as e:
            db.session.rollback()
            logging.critical(str(e))
            return {"error": "não foi possível registrar o usuário"}, 500


# Recuperação de e-mail temporária
class ForgetPassword(Resource):
    def post(self):
        parser = reqparse.RequestParser(trim=True)
        parser.add_argument("email", required=True, help="o campo email é obrigatório")
        args = parser.parse_args()

        user = User.query.filter_by(email=args.email).first()
        if not user:
            return {"error": "e-mail não encontrado!"}, 404

        temp_password = secrets.token_hex(8)
        user.password = generate_password_hash(temp_password)
        db.session.add(user)
        db.session.commit()
        send_mail(
            "Recuperação de conta",
            user.email,
            "forgot-password",
            temp_password,
        )
        return {"success", "E-mail enviado com sucesso."}, 200
