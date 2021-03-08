from werkzeug.exceptions import HTTPException
from http import HTTPStatus


class MalFormedException(HTTPException):
    code = HTTPStatus.BAD_REQUEST
    description = 'Malformed request'
