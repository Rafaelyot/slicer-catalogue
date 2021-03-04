import os

from mongoengine import connect
from mixer.backend.mongoengine import TypeMixer, Mixer
from models.descriptors import Nsd
from models.vsblueprint import VsdNsdTranslationRule, VsBlueprint
from models.catalogues import OnBoardVnfPackageRequest

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
        # Avoid MapFields due to mixer's errors
        return field.scheme.__class__.__name__ != 'MapField'


class MyMixer(Mixer):
    def __init__(self, **params):
        self.type_mixer_cls = MyTypeMixer
        super(MyMixer, self).__init__(**params)


mixer = MyMixer()

for _ in range(5):
    nsd = mixer.blend(Nsd)
    vsd_nsd_translation_rule = mixer.blend(VsdNsdTranslationRule)
    on_board_vnf_package_request = mixer.blend(OnBoardVnfPackageRequest)
    vs_blueprint = mixer.blend(VsBlueprint)
