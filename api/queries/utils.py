from mongoengine import DoesNotExist, MultipleObjectsReturned
from exceptions.utils import HTTPException
from http import HTTPStatus
import re


def exception_message_elements(cls, **kwargs):
    """
    @param cls: Class object
    @param kwargs: Query's arguments
    @return: a tuple with the class name and concatenation of args in string
    """
    class_name = ' '.join(re.findall('[A-Z][^A-Z]*', cls.__name__))

    args = []
    for arg_name, arg_value in kwargs.items():
        args += [arg_name, arg_value]

    return class_name, " ".join(args)


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
