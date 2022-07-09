from flask_restful import reqparse


def register_prs():
    parser = reqparse.RequestParser()
    parser.add_argument("email", required=True, help="o campo email é obrigatório.")
    parser.add_argument(
        "password", required=True, help="o campo password é obrigatório."
    )
    return parser.parse_args()


def forgot_passw_prs():
    parser = reqparse.RequestParser()
    parser.add_argument("email", required=True, help="o campo email é obrigatório.")
    return parser.parse_args()


def profile_prs():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "first_name",
        required=True,
        help="o campo first_name é obrigatório",
    )
    parser.add_argument(
        "last_name", required=True, help="o campo last_name é obrigatório"
    )
    parser.add_argument("cpf", required=True, help="o campo cpf é obrigatório")
    parser.add_argument("phone", required=True, help="o campo phone é obrigatório")
    return parser.parse_args()


def order_create_prs():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "product_id",
        required=True,
        help="o campo product_id é obrigatório",
    )
    parser.add_argument("quatity", required=True, help="o campo quatity é obrigatório")
    return parser.parse_args()
