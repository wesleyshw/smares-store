from flask_restful import reqparse


def register_prs():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "email", required=True, help="o campo email é obrigatório."
    )
    parser.add_argument(
        "password", required=True, help="o campo password é obrigatório."
    )
    return parser.parse_args()


def forgot_passw_prs():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "email", required=True, help="o campo email é obrigatório."
    )
    return parser.parse_args()
