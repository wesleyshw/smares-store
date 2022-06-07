from flask_restful import Api

from app.resources import auth
from app.resources import product


def init_app(app):
    api = Api(app, prefix="/api")
    api.add_resource(auth.Login, "/auth/login")
    api.add_resource(auth.Register, "/auth/register")
    api.add_resource(auth.ForgetPassword, "/auth/forget-password")

    api.add_resource(product.ProductList, "/products")
    api.add_resource(product.ProductGet, "/products/<slug>")
