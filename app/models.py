from app.extensions import db


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer)
    email = db.Column(db.String(84), nullalbe=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return self.email
