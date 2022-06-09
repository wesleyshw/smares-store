import logging
from random import getrandbits

from app.extensions import db
from app.models import Item, Order, Product
from app.schemas import order_fields
from app.services.auth import jwt_auth
from flask_jwt_extended import current_user
from flask_restful import Resource, marshal, reqparse


class Create(Resource):
    @jwt_auth()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "product_id", required=True, help="o campo product_id é obrigatório"
        )
        parser.add_argument(
            "quatity", required=True, help="o campo quatity é obrigatório"
        )
        args = parser.parse_args()
        if not current_user:
            return {"error": "Acesso negado, faça o login."}, 400

        product = Product.query.get(args.product_id)
        if not product:
            return {"error": "produto não encontrado!"}, 404
        if args.quantity > product.quantity:
            return {"error": "não possuímos essa quantidade."}, 400

        try:
            order = Order()
            order.reference_id = f"SMARES-{getrandbits(20)}"
            db.session.add(order)
            db.session.commit()

            item = Item()
            item.order_id = order.id
            item.product_id = product.id
            item.user_id = current_user.id
            item.quantity = args.quantity
            item.price = product.price * args.quantity
            db.session.add(item)
            db.session.commit()

            return marshal(order, order_fields, "order")
        except Exception as e:
            logging.critical(str(e))
            db.session.rollback()
            return {"error": "Não foi possível criar o seu pedido."}, 500


class Pay(Resource):
    pass


class Notification(Resource):
    pass
