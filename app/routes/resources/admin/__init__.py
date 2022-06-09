from app.routes.resources.admin import auth


def init_api(api):
    api.add_resource(auth.Login, "/auth/login")
