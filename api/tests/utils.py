from mixer.backend.marshmallow import BaseTypeMixer, GenFactory, t, ValidationError, LOGGER, fields, faker, validate, \
    partial, BaseMixer, SKIP_VALUE, missing, TypeMixer, Mixer
import functools
import subprocess
import pytest


def catch_exception(func):
    """
    Returns:
        object:
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        worker = kwargs['error_catcher']
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print('stdout:', worker.stdout.read().decode("utf-8"))
            print('stderr:', worker.stderr.read().decode("utf-8"))
            raise

    return wrapper


@pytest.fixture(scope='module')
def error_catcher(request) -> subprocess.Popen:
    """py.test fixture to create app scaffold."""
    cmdline = ["echo", "ERROR!!"]

    worker = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    worker.wait(timeout=5.0)

    return worker


class TestTypeMixer(TypeMixer):
    def __init__(self, cls, **params):
        delattr(TypeMixer, 'is_required')
        # delattr(TypeMixer, 'gen_field')
        super(TestTypeMixer, self).__init__(cls, **params)

    def is_required(self, field):
        # Avoid dict generations errors
        #
        return field.scheme.__class__.__name__ != 'Dict'


class TestMixer(Mixer):
    def __init__(self, **params):
        self.type_mixer_cls = TestTypeMixer
        params.setdefault('required', False)
        super(TestMixer, self).__init__(**params)


# class TypeMixer(BaseTypeMixer):
#     """ TypeMixer for Marshmallow. """
#
#     factory = GenFactory
#
#     def __load_fields(self):
#         for name, field in self.__scheme._declared_fields.items():
#             yield name, t.Field(field, name)
#
#     def is_required(self, field):
#         """ Return True is field's value should be defined.
#
#         :return bool:
#
#         """
#         return field.scheme.__class__.__name__ != 'Dict'
#         # return field.scheme.required or (
#         #         self.__mixer.params['required'] and not field.scheme.dump_only)
#
#     @staticmethod
#     def get_default(field):
#         """ Get default value from field.
#
#         :return value:
#
#         """
#         return field.scheme.default is missing and SKIP_VALUE or field.scheme.default  # noqa
#
#     def populate_target(self, values):
#         """ Populate target. """
#         try:
#             return self.__scheme().load(dict(values))
#         except ValidationError as exc:
#             LOGGER.error("Mixer-marshmallow: %r", exc.messages)
#             return
#
#     def make_fabric(self, field, field_name=None, fake=False, kwargs=None):  # noqa
#         kwargs = {} if kwargs is None else kwargs
#
#         if isinstance(field, fields.Nested):
#             kwargs.update({'_typemixer': self, '_scheme': type(field.schema), '_many': field.many})
#
#         if isinstance(field, fields.List):
#             fab = self.make_fabric(
#                 field.inner, field_name=field_name, fake=fake, kwargs=kwargs)
#             return lambda: [fab() for _ in range(faker.small_positive_integer(4))]
#
#         for validator in field.validators:
#             if isinstance(validator, validate.OneOf):
#                 return partial(faker.random_element, validator.choices)
#
#         return super(TypeMixer, self).make_fabric(
#             type(field), field_name=field_name, fake=fake, kwargs=kwargs)
#
#
# class Mixer(BaseMixer):
#     """ Integration with Marshmallow. """
#
#     type_mixer_cls = TypeMixer
#
#     def __init__(self, *args, **kwargs):
#         super(Mixer, self).__init__(*args, **kwargs)
#
#         # All fields is required by default
#         self.params.setdefault('required', True)


mixer = TestMixer()
