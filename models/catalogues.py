from mongoengine import Document
from mongoengine.fields import StringField, MapField


class OnBoardVnfPackageRequest(Document):
    name = StringField()
    version = StringField()
    provider = StringField()
    checksum = StringField()
    user_defined_data = MapField(StringField())
    vnf_package_path = StringField()
