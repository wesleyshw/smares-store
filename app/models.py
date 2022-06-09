from datetime import datetime
from app.enums import EStatus
from app.extensions import db


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(84), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)
    items = db.relationship("Item", backref="user", uselist=True)
    profile = db.relationship("Profile", backref="user", uselist=False)

    def __repr__(self):
        return self.email

    @classmethod
    def find_by_email(cls, email):
        return User.query.filter_by(email=email).first()


class Profile(db.Model):

    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    cpf = db.Column(db.String(60), nullable=False, unique=True, index=True)
    phone = db.Column(db.String(60), nullable=False, unique=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return self.first_name + self.last_name


class Product(db.Model):

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(140), nullable=False, unique=True, index=True)
    price = db.Column(db.Float, nullable=False)
    # image = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    created_at = db.Column(db.DateTime, default=datetime.now)
    items = db.relationship("Item", backref="product", uselist=True)

    def __repr__(self):
        return self.name

    @classmethod
    def find_by_slug(cls, slug):
        return Product.query.filter_by(slug=slug).first()


class Category(db.Model):

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    slug = db.Column(db.String(45), nullable=False, unique=True, index=True)
    products = db.relationship("Product", backref="categories", uselist=True)

    def __repr__(self):
        return self.name


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    reference_id = db.Column(db.String(130), nullable=False)
    status = db.Column(db.String(40), default=EStatus.OPENED.value, nullable=False)
    item = db.relationship("Item", backref="order", uselist=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"order number:{self.reference_id}"


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"order number: ${self.order.number} quantity: {self.quantity} user: {self.user.profile.first_name} {self.user.profile.last_name}"
