from marshmallow import Schema, validate
from marshmallow.fields import String, List, Boolean, Integer, Dict, Nested
from api.enums.ns_descriptor import NsScaleType, ScalingProcedureType, LogicOperation, RelationalOperation
from api.enums.descriptor import LayerProtocol, CpRole
from api.serializers.descriptor import AddressDataSerializer, ConnectivityTypeSerializer, VirtualLinkDfSerializer, \
    QoSSerializer, MonitoringParameterSerializer, AffinityRuleSerializer, LinkBitrateRequirementsSerializer, \
    VirtualLinkProfileSerializer, AffinityOrAntiAffinityGroupSerializer, LifeCycleManagementScriptSerializer


class SapdSerializer(Schema):
    cpi_id = String()
    layer_protocol = String(validate=validate.OneOf(LayerProtocol.get_values()))
    cp_role = String(validate=validate.OneOf(CpRole.get_values()))
    description = String()
    address_data = List(Nested(AddressDataSerializer))
    sap_address_assignment = Boolean()
    ns_virtual_link_desc_id = String()
    associated_cdp_id = String()


class SecurityParametersSerializer(Schema):
    signature = String()
    algorithm = String()
    certificate = String()


class NsVirtualLinkDescSerializer(Schema):
    virtual_link_desc_id = String()
    virtual_link_desc_provider = String()
    virtual_link_desc_version = String()
    connectivity_type = Nested(ConnectivityTypeSerializer)
    virtual_link_df = List(Nested(VirtualLinkDfSerializer))
    test_access = List(String())
    description = String()
    security = Nested(SecurityParametersSerializer)


class NfpdSerializer(Schema):
    nfp_id = String()
    # nfp_rule =
    cpd = List(String())
    qos = Nested(QoSSerializer)


class VnffgdSerializer(Schema):
    vnffgd_id = String()
    vnfd_id = List(String())
    pnfd_id = List(String())
    virtual_link_desc_id = List(String())
    cpd_pool_id = List(String())
    nfpd = List(Nested(NfpdSerializer))


class VnfIndicatorDataSerializer(Schema):
    vnfd_id = String()
    vnf_indicator = String()


class MonitoredDataSerializer(Schema):
    vnf_indicator_info = Nested(VnfIndicatorDataSerializer)
    monitoring_parameter = Nested(MonitoringParameterSerializer)


class NsScaleInfoSerializer(Schema):
    ns_scaling_aspect_id = String()
    ns_scale_level_Id = String()


class ScaleNsToLevelDataSerializer(Schema):
    ns_instantiation_level = String()
    ns_scale_info = List(Nested(NsScaleInfoSerializer))


class AutoscalingActionSerializer(Schema):
    scale_type = String(validate=validate.OneOf(NsScaleType.get_values()))
    scale_ns_to_level_data = Nested(ScaleNsToLevelDataSerializer)


class AutoscalingRuleCriteriaSerializer(Schema):
    name = String()
    scale_in_threshold = Integer()
    scale_in_relational_operation = String(validate=validate.OneOf(RelationalOperation.get_values()))
    scale_out_threshold = Integer()
    scale_out_relational_operation = String(validate=validate.OneOf(RelationalOperation.get_values()))
    ns_monitoring_param_ref = String()


class AutoscalingRuleConditionSerializer(Schema):
    name = String()
    scaling_type = String(validate=validate.OneOf(ScalingProcedureType.get_values()))
    enabled = Boolean()
    scale_in_operation_type = String(validate=validate.OneOf(LogicOperation.get_values()))
    scale_out_operation_type = String(validate=validate.OneOf(LogicOperation.get_values()))
    threshold_time = Integer()
    cooldown_time = Integer()
    initial_instantiation_level = String()
    scaling_criteria = List(Nested(AutoscalingRuleCriteriaSerializer))


class NsAutoscalingRuleSerializer(Schema):
    rule_id = String()
    rule_condition = Nested(AutoscalingRuleConditionSerializer)
    rule_actions = List(Nested(AutoscalingActionSerializer))


class NsVirtualLinkConnectivitySerializer(Schema):
    virtual_link_profile_id = String()
    cpd_id = List(String())


class VnfConfigurationScriptSerializer(Schema):
    args = Dict(keys=String(), values=String())
    script = List(String())


class VnfLCMScriptsSerializer(Schema):
    target = String()
    scripts = Dict(keys=String(), values=Nested(VnfConfigurationScriptSerializer))


class VnfProfileSerializer(Schema):
    vnf_profile_id = String()
    vnfd_id = String()
    flavour_id = String()
    instantiation_level = String()
    min_number_of_instances = Integer()
    max_number_of_instances = Integer()
    local_affinity_or_anti_affinity_rule = List(Nested(AffinityRuleSerializer))
    affinity_or_anti_affinity_group_id = List(String())
    ns_virtual_link_connectivity = List(Nested(NsVirtualLinkConnectivitySerializer))
    script = List(Nested(VnfLCMScriptsSerializer))


class PnfProfileSerializer(Schema):
    pnf_profile_id = String()
    pnfd_id = String()
    ns_virtual_link_connectivity = List(Nested(NsVirtualLinkConnectivitySerializer))


class VnfToLevelMappingSerializer(Schema):
    vnf_profile_id = String()
    number_of_instances = Integer()


class NsToLevelMappingSerializer(Schema):
    ns_profile_id = String()
    number_of_instances = Integer()


class VirtualLinkToLevelMappingSerializer(Schema):
    virtual_link_profile_id = String()
    bit_rate_requirements = Nested(LinkBitrateRequirementsSerializer)


class NsLevelSerializer(Schema):
    ns_level_id = String()
    description = String()
    vnf_to_level_mapping = List(Nested(VnfToLevelMappingSerializer))
    ns_to_level_mapping = List(Nested(NsToLevelMappingSerializer))
    virtual_link_to_level_mapping = List(Nested(VirtualLinkToLevelMappingSerializer))


class NsScalingAspectSerializer(Schema):
    ns_scaling_aspect_id = String()
    name = String()
    description = String()
    ns_scale_level = List(Nested(NsLevelSerializer))


class NsProfileSerializer(Schema):
    ns_profile_id = String()
    nsd_id = String()
    ns_deployment_flavour_id = String()
    ns_instantiation_level_id = String()
    min_number_of_instances = Integer()
    max_number_of_instances = Integer()
    affinity_or_anti_affinity_group_id = List(String())
    ns_virtual_link_connectivity = List(Nested(NsVirtualLinkConnectivitySerializer))


class DependenciesSerializer(Schema):
    primary_id = List(String())
    secondary_id = List(String())


class NsDfSerializer(Schema):
    ns_df_id = String()
    flavour_key = String()
    vnf_profile = List(Nested(VnfProfileSerializer))
    pnf_profile = List(Nested(PnfProfileSerializer))
    virtual_link_profile = List(Nested(VirtualLinkProfileSerializer))
    scaling_aspect = List(Nested(NsScalingAspectSerializer))
    affinity_or_anti_affinity_group = List(Nested(AffinityOrAntiAffinityGroupSerializer))
    ns_instantiation_level = List(Nested(NsLevelSerializer))
    default_ns_instantiation_level_id = String()
    ns_profile = List(Nested(NsProfileSerializer))
    dependencies = List(Nested(DependenciesSerializer))


class NsdSerializer(Schema):
    nsd_identifier = String()
    designer = String()
    version = String()
    nsd_name = String()
    nsd_invariant_id = String()
    nested_id = List(String())
    vnfd_id = List(String())
    pnfd_id = List(String())
    sapd = List(Nested(SapdSerializer))
    virtual_link_desc = List(Nested(NsVirtualLinkDescSerializer))
    vnffgd = List(Nested(VnffgdSerializer))
    monitored_info = List(Nested(MonitoredDataSerializer))
    auto_scaling_rule = List(Nested(NsAutoscalingRuleSerializer))
    life_cycle_management_script = List(Nested(LifeCycleManagementScriptSerializer))
    ns_df = List(Nested(NsDfSerializer))
    security = Nested(SecurityParametersSerializer)
