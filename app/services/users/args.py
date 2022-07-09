from app.services.all.response import msg


def register_args(args):
    for value in args:
        if args[value] == "":
            return msg("error", "Preencha todos os campos!", 406)
        if args[value] == None:
            return msg("error", "Insira os dados corretamente!", 400)


def forgot_passw_args(args):
    for value in args:
        if args[value] == "":
            return msg("error", "Preencha todos os campos!", 406)
        if args[value] == None:
            return msg("error", "Insira os dados corretamente!", 400)
