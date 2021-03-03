import os

from mongoengine import connect
from mixer.backend.mongoengine import TypeMixer, Mixer, t
from models.descriptors import Nsd

connection_data = {
    'username': os.environ.get('MONGO_USERNAME', 'root'),
    'password': os.environ.get('MONGO_PASSWORD', 'root'),
    'host': os.environ.get('MONGO_URL', 'localhost'),
    'port': 27017,
    'db': os.environ.get('MONGO_DB', 'catalogues'),
    'authentication_source': 'admin'
}

connect(**connection_data)


class MyTypeMixer(TypeMixer):
    def __init__(self, cls, **params):
        super(MyTypeMixer, self).__init__(cls, **params)

    @staticmethod
    def is_required(field):
        return True

    # noinspection PyPep8Naming,PyProtectedMember
    def _TypeMixer__load_fields(self):
        scheme = self._TypeMixer__scheme

        if not hasattr(scheme, '_fields'):
            yield ()

        for f_name, field in scheme._fields.items():
            yield f_name, t.Field(field, f_name)


class MyMixer(Mixer):
    def __init__(self, **params):
        self.type_mixer_cls = MyTypeMixer
        super(MyMixer, self).__init__(**params)


mixer = MyMixer()
nsd = mixer.blend(Nsd)
