from marshmallow import Schema
from marshmallow.fields import String, List, Boolean, Dict, Nested
from api.enums.vs_descriptor import ServiceCreationTimeRange, AvailabilityCoverageRange, SliceManagementControlType


class ServiceConstraintsSerializer(Schema):
    sharable = Boolean()
    include_shared_elements = Boolean()
    preferred_providers = List(String())
    non_preferred_providers = List(String())
    prohibited_providers = List(String())
    atomic_component_id = String()


class VsdSlaSerializer(Schema):
    service_creation_time = String(choices=ServiceCreationTimeRange.get_values())
    availability_coverage = String(choices=AvailabilityCoverageRange.get_values())
    low_cost_required = Boolean()


class VsDescriptorSerializer(Schema):
    descriptor_id = String()
    name = String(required=True, error_messages={"required": "VSD without name"})
    version = String(required=True, error_messages={"required": "VSD without version"})
    vs_blueprint_id = String(required=True, error_messages={"required": "VSD without VS blueprint ID"})
    management_type = String(choices=SliceManagementControlType.get_values())
    qos_parameters = Dict(keys=String(), values=String())
    is_public = Boolean()
    tenant_id = String()
    service_constraints = List(Nested(ServiceConstraintsSerializer))
    sla = Nested(VsdSlaSerializer)
    # TODO: Check sliceServiceParameters
    nested_vsd_ids = Dict(keys=String(), values=String())
    associated_vsd_id = String()
    domain_id = String()
