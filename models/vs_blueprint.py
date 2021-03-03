from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import StringField, IntField, EmbeddedDocumentListField, ListField, MapField, EnumField, \
    BooleanField
from enums.vs_blueprint import VsComponentPlacement, VsComponentType, MetricCollectionType, SliceServiceType, \
    EMBBServiceCategory, URLLCServiceCategory


# vnfPackages
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


# vsBlueprint
class VsBlueprintParameter(EmbeddedDocument):
    parameter_id = StringField()
    parameter_name = StringField()
    parameter_type = StringField()
    parameter_description = StringField()
    applicability_field = StringField()


class VsComponent(EmbeddedDocument):
    component_id = StringField()
    servers_number = IntField()
    image_urls = ListField(StringField())
    end_points_ids = ListField(StringField())
    lifecycleOperations = MapField(StringField())
    placement = EnumField(VsComponentPlacement)
    type = EnumField(VsComponentType)
    associated_vsb_id = StringField()
    compatible_site = StringField()


class VsbForwardingPathEndPoint(EmbeddedDocument):
    vs_component_id = StringField()
    endPoint_id = StringField()


class VsbEndpoint(EmbeddedDocument):
    end_point_id = StringField()
    external = BooleanField()
    management = BooleanField()
    ran_connection = BooleanField()


class VsbLink(EmbeddedDocument):
    end_point_ids = ListField(StringField())
    external = BooleanField()
    name = StringField()
    connectivity_properties = ListField(StringField())


class ApplicationMetric(EmbeddedDocument):
    topic = StringField()
    metric_id = StringField()
    name = StringField()
    metric_collection_type = EnumField(MetricCollectionType)
    unit = StringField()
    interval = StringField()


class VsBlueprint(Document):
    blueprint_id = StringField()
    version = StringField()
    name = StringField()
    description = StringField()
    parameters = EmbeddedDocumentListField(VsBlueprintParameter)
    atomic_components = EmbeddedDocumentListField(VsComponent)
    service_sequence = EmbeddedDocumentListField(VsbForwardingPathEndPoint)
    end_points = EmbeddedDocumentListField(VsbEndpoint)
    connectivity_services = EmbeddedDocumentListField(VsbLink)
    configurable_parameters = ListField(StringField())
    application_metrics = EmbeddedDocumentListField(ApplicationMetric)
    inter_site = BooleanField()
    slice_service_type = EnumField(SliceServiceType)
    embb_service_category = EnumField(EMBBServiceCategory)
    urllc_service_category = EnumField(URLLCServiceCategory)
