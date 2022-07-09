from flask import jsonify, make_response


def msg(type, msg, code):
    message = jsonify({"type": type, "msg": msg, "code": code})
    response = make_response(message, code)
    return response
