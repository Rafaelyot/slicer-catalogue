from http import HTTPStatus
from flask import jsonify


def response_template(message, data=None, status_code=HTTPStatus.OK):
    if data is None:
        data = []
    return jsonify({
        'message': message,
        'data': data
    }), status_code
