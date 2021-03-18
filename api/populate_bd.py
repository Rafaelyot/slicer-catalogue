import os

from mongoengine import connect
from mixer.backend.mongoengine import TypeMixer, Mixer
from models.descriptors import Nsd
from models.vs_blueprint import VsdNsdTranslationRule, VsBlueprint, VsBlueprintInfo
from models.catalogues import OnBoardVnfPackageRequest

connection_data = {
    # 'username': os.environ.get('MONGO_USERNAME', 'root'),
    # 'password': os.environ.get('MONGO_PASSWORD', 'root'),
    'host': os.environ.get('MONGO_URL', 'localhost'),
    'port': 27017,
    'db': os.environ.get('MONGO_DB', 'catalogues'),
    # 'authentication_source': 'admin',
    # 'replicaSet': 'rs0'
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

for i in range(5):
    nsd = mixer.blend(Nsd)
    vsd_nsd_translation_rule = mixer.blend(VsdNsdTranslationRule)
    on_board_vnf_package_request = mixer.blend(OnBoardVnfPackageRequest)
    vs_blueprint = mixer.blend(VsBlueprint, blueprint_id=f'id_{i}', version=f'version_{i}', name=f'name_{i}')
    vs_blueprint_info = mixer.blend(VsBlueprintInfo, vs_blueprint_id=f'id_{i}', vs_blueprint_version=f'version_{i}',
                                    name=f'name_{i}', active_vsd_id=[])
