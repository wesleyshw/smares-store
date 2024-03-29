import logging
import secrets
from base64 import b64decode
from datetime import timedelta

from app.extensions import db
from app.models import User
from app.services.all.mail import send_mail
from app.services.users.args import *
from app.services.users.parsers import *
from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash, generate_password_hash


class Login(Resource):
    def get(self):
        if not request.headers.get("Authorization"):
            return msg("error", "Preencha o Headers com Authorization.", 400)
        basic, code = request.headers["Authorization"].split(" ")
        if not basic.lower() == "basic":
            return msg("error", "Authorization mal formatado!", 400)

        email, password = b64decode(code).decode().split(":")
        if email == "":
            return msg("error", "O campo de email é obrigatório.", 400)
        if password == "":
            return msg("error", "O campo de password é obrigatório.", 400)

        user = User.query.filter_by(email=email).first()
        if not user:
            return msg("error", "E-mail não encontrado.", 404)
        if not check_password_hash(user.password, password):
            return msg("error", "Senha incorreta.", 400)

        token = create_access_token({"id": user.id}, expires_delta=timedelta(days=30))

        return msg("success", token, 201)


class Register(Resource):
    def post(self):
        args = register_prs()
        check = register_args(args)
        if check:
            return check
        user = User.query.filter_by(email=args.email).first()
        if user:
            return msg("error", "E-mail já registrado.", 400)

        user = User()
        user.email = args.email
        user.password = generate_password_hash(args.password, salt_length=10)
        db.session.add(user)

        try:
            db.session.commit()
            # deixar o send_mail desativado por enquando para testar depois
            # send_mail(
            #     "Bem vindo(a) à Smares Store",
            #     user.email,
            #     "welcome",
            #     email=user.email,
            # )
            return msg("success", "Usuário registrado com sucesso.", 201)
        except Exception as e:
            db.session.rollback()
            logging.critical(str(e))
            return msg("error", "Não foi possível registrar o usuário.", 500)


# Atualizar a recuperação para duas etapas mais pra frente
class ForgetPassword(Resource):
    def post(self):
        args = forgot_passw_prs()
        check = forgot_passw_args(args)
        if check:
            return check

        user = User.query.filter_by(email=args.email).first()
        if not user:
            return msg("error", "E-mail não encontrado!", 404)

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
        return msg("success", "E-mail enviado com sucesso.", 200)
