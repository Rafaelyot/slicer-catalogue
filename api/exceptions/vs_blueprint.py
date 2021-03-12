from werkzeug.exceptions import HTTPException
from http import HTTPStatus


class MalFormedException(HTTPException):
    code = HTTPStatus.BAD_REQUEST
    description = 'Malformed request'


class FailedOperationException(HTTPException):
    code = HTTPStatus.CONFLICT
    description = 'There are some VSDs associated to the VS Blueprint. Impossible to remove it.'


class BadVsBlueprintBody(HTTPException):
    code = HTTPStatus.BAD_REQUEST

    def __init__(self, description):
        self.description = description


class AlreadyExistingEntityException(HTTPException):
    code = HTTPStatus.CONFLICT

    def __init__(self, description):
        self.description = description
