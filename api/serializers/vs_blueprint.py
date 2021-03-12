from marshmallow import Schema
from marshmallow.fields import String, List, Boolean, Integer, Dict, Nested

from enums.vs_blueprint import SliceServiceType, EMBBServiceCategory, URLLCServiceCategory, MetricCollectionType, \
    VsComponentPlacement, VsComponentType


class VsdParameterValueRange(Schema):
    parameter_id = String()
    min_value = Integer()
    max_value = Integer()


class VsdNsdTranslationRule(Schema):
    input = List(Nested(VsdParameterValueRange))
    blueprint_id = String()
    nst_id = String()
    nsd_id = String()
    nsd_version = String()
    ns_flavour_id = String()
    ns_instantiation_level_id = String()
    nsd_info_id = String()


class VsBlueprintParameter(Schema):
    parameter_id = String()
    parameter_name = String()
    parameter_type = String()
    parameter_description = String()
    applicability_field = String()


class VsComponent(Schema):
    component_id = String()
    servers_number = Integer()
    image_urls = List(String())
    end_points_ids = List(String())
    lifecycleOperations = Dict(keys=String(), values=String())
    placement = String(choices=VsComponentPlacement.get_values())
    type = String(choices=VsComponentType.get_values())
    associated_vsb_id = String()
    compatible_site = String()


class VsbForwardingPathEndPoint(Schema):
    vs_component_id = String()
    endPoint_id = String()


class VsbEndpoint(Schema):
    end_point_id = String()
    external = Boolean()
    management = Boolean()
    ran_connection = Boolean()


class VsbLink(Schema):
    end_point_ids = List(String())
    external = Boolean()
    name = String()
    connectivity_properties = List(String())


class ApplicationMetric(Schema):
    topic = String()
    metric_id = String()
    name = String()
    metric_collection_type = String(choices=MetricCollectionType.get_values())
    unit = String()
    interval = String()


class VsBlueprintSerializer(Schema):
    blueprint_id = String()
    version = String(required=True)
    name = String(required=True)
    description = String()
    parameters = List(Nested(VsBlueprintParameter))
    atomic_components = List(Nested(VsComponent))
    service_sequence = List(Nested(VsbForwardingPathEndPoint))
    end_points = List(Nested(VsbEndpoint))
    connectivity_services = List(Nested(VsbLink))
    configurable_parameters = List(String())
    application_metrics = List(Nested(ApplicationMetric))
    inter_site = Boolean()
    slice_service_type = String(choices=SliceServiceType.get_values())
    embb_service_category = String(choices=EMBBServiceCategory.get_values())
    urllc_service_category = String(choices=URLLCServiceCategory.get_values())


class VsBlueprintInfoSerializer(Schema):
    vs_blueprint = Nested(VsBlueprintSerializer)
    vs_blueprint_id = String()
    vs_blueprint_version = String()
    name = String()
    owner = String()
    on_boarded_nsd_info_id = List(String())
    on_boarded_nst_info_id = List(String())
    on_boarded_vnf_package_info_id = List(String())
    on_boarded_mec_app_package_info_id = List(String())
    active_vsd_id = List(String())
