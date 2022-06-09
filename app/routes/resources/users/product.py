from flask_restful import Resource, marshal, marshal_with

from app.models import Product
from app.schemas import product_fields


class ProductList(Resource):
    @marshal_with(product_fields, "products")
    def get(self):
        products = Product.query.all()
        return products


class ProductGet(Resource):
    def get(self, slug):
        product = Product.query.filter_by(slug=slug).first()
        if not product:
            return {"error": "produto não encontrado!"}, 404
        return marshal(product, product_fields, "product")
