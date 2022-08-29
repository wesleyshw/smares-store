from app.routes.resources.users import auth
from app.routes.resources.users import product
from app.routes.resources.users import order
from app.routes.resources.users import user


def init_api(api):
    api.add_resource(auth.Login, "/auth/login")
    api.add_resource(auth.Register, "/auth/register")
    api.add_resource(auth.ForgetPassword, "/auth/forget-password")

    api.add_resource(product.ProductList, "/products")
    api.add_resource(product.ProductGet, "/products/<slug>")

    api.add_resource(order.Create, "/order/create")
    api.add_resource(order.Pay, "/order/pay")
    api.add_resource(order.Notification, "/order/notification")

    api.add_resource(user.Orders, "/user/orders")
