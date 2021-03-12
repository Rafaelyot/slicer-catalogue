from mongoengine import DoesNotExist, MultipleObjectsReturned
from exceptions.utils import HTTPException
from http import HTTPStatus
from flask_mongoengine import current_mongoengine_instance
from exceptions.utils import exception_message_elements


def get_or_error(cls, status_code=HTTPStatus.NOT_FOUND, **kwargs):
    """
    @param cls: Model to be queried
    @param status_code: Http status code returned whenever a 'DoesNotExist' or 'MultipleObjectsReturned' exception is thrown
    @param kwargs: Query's arguments
    @return: Retrieve the the matching object raising an HttpException if multiple results or no results are found
    """

    try:
        return cls.objects.get(**kwargs)

    except DoesNotExist:
        class_name, args = exception_message_elements(cls, **kwargs)

        e = HTTPException(f"{class_name} with {args} not found in DB")
        e.code = status_code
        raise e

    except MultipleObjectsReturned:
        class_name, args = exception_message_elements(cls, **kwargs)

        e = HTTPException(f"Found multiple {class_name} objects with {args} in DB")
        e.code = status_code
        raise e


def transaction(callback):
    db = current_mongoengine_instance().connection
    with db.start_session() as session:
        session.with_transaction(callback)
