from flask_jwt_extended import verify_jwt_in_request
from functools import wraps
from flask import current_app, jsonify, make_response
from app.extensions import db, jwt
from app.models import User


def msg(type, msg, code):
    message = jsonify({"type": type, "msg": msg, "code": code})
    response = make_response(message, code)
    return response


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    id = jwt_data["sub"]["id"]
    # if jwt_data["sub"]["passar o tipo do usuário"] == "valor em token_hex":
    return User.query.filter_by(id=id).one_or_none()


def jwt_auth(optional=False):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            user = verify_jwt_in_request(optional)
            if hasattr(current_app, "ensure_sync") and callable(
                getattr(current_app, "ensure_sync", None)
            ):
                # checar o valor da variável user caso for o token_hex
                # do determinado tipo de usuáriofazer a validação caso
                # contrário o retornar uma response de redirecionamento,
                # ou então vai retornar acesso negado.
                if user:
                    return current_app.ensure_sync(fn)(*args, **kwargs)
                if not user:
                    return msg("error", "Acesso negado, faça o login.", 401)
                return msg("error", "Acesso negado, faça o login.", 401)

            return fn(*args, **kwargs)

        return decorator

    return wrapper
