from werkzeug.exceptions import HTTPException
from views.utils import response_template
from http import HTTPStatus


def handle_exception(app):
    @app.errorhandler(Exception)
    def decorator(e):
        if isinstance(e, Exception):  # Ignore startup call
            if isinstance(e, HTTPException):  # If it is a Http Error
                return response_template(message=e.description, status_code=e.code)

            # If it is a python Error
            return response_template(message=f'Internal exception - {e}', status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

    return decorator
