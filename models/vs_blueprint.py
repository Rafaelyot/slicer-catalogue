from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import StringField, IntField, EmbeddedDocumentListField


class VsdParameterValueRange(EmbeddedDocument):
    parameter_id = StringField()
    min_value = IntField()
    max_value = IntField()


class VsdNsdTranslationRule(Document):
    input = EmbeddedDocumentListField(VsdParameterValueRange)
    blueprint_id = StringField()
    nst_id = StringField()
    nsd_id = StringField()
    nsd_version = StringField()
    ns_flavour_id = StringField()
    ns_instantiation_level_id = StringField()
    nsd_info_id = StringField()
