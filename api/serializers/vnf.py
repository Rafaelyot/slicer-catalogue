from marshmallow import Schema, pre_load, ValidationError
from marshmallow.fields import String, Dict, Url, Nested, List,Integer, Boolean

from api.enums.vnf import VnfIndicatorSource
from api.enums.descriptor import OperationalState, UsageState, \
    VnfLcmOperation
from api.serializers.descriptor import CpdSerializer, VirtualNetworkInterfaceRequirementsSerializer, \
    SwImageDescSerializer, VirtualStorageDescSerializer, \
    VirtualComputeDescSerializer, ConnectivityTypeSerializer, VirtualLinkDfSerializer, MonitoringParameterSerializer, \
    AffinityRuleSerializer, VirtualLinkProfileSerializer, ScaleInfoSerializer, TerminateVnfOpConfigSerializer, \
    AffinityOrAntiAffinityGroupSerializer, LifeCycleManagementScriptSerializer


class OnBoardVnfPackageRequestSerializer(Schema):
    name = String(required=True, error_messages={"required": "On board VNF package request without name"})
    version = String(required=True, error_messages={"required": "On board VNF package request without version"})
    provider = String(required=True, error_messages={"required": "On board VNF package request without provider"})
    checksum = String(required=True, error_messages={"required": "On board VNF package request without checksum"})
    user_defined_data = Dict(keys=String(), values=String())
    vnf_package_path = Url(required=True,
                           error_messages={"required": "On board VNF package request without package path"})


class SoftwareImageInformationSerializer(Schema):
    software_image_id = String(required=True, error_messages={"required": "Sw image info without ID"})
    name = String(required=True, error_messages={"required": "Sw image info without name"})
    provider = String()
    version = String()
    checksum = String()
    container_format = String()
    disk_format = String()
    created_at = Integer() # Unix Time
    min_disk = Integer()
    min_ram = Integer()
    size = Integer()
    user_metadata = Dict(keys=String(), values=String())


class VnfPackageSoftwareImageInformationSerializer(Schema):
    access_information = String(required=True,
                                error_messages={"required": "VNF package sw image info without access information"})
    software_image_information = Nested(SoftwareImageInformationSerializer, required=True, error_messages={
        "required": "VNF package sw image info without sw image information"})


class VnfPackageArtifactInformationSerializer(Schema):
    selector = String(required=True, error_messages={"required": "VNF package artifact information without selector"})
    metadata = String(required=True, error_messages={"required": "VNF package artifact information without metadata"})


class OnboardedVnfPkgInfoSerializer(Schema):
    onboarded_vnf_pkg_info_id = String(required=True,
                                       error_messages={"required": "Onboarded VNF package info without ID"})
    vnfd_id = String(required=True, error_messages={"required": "Onboarded VNF package info without VNFD ID"})
    vnf_provider = String(required=True, error_messages={"required": "Onboarded VNF package info without VNF provider"})
    vnf_product_name = String(required=True,
                              error_messages={"required": "Onboarded VNF package info without VNF product name"})
    vnf_software_version = String(required=True,
                                  error_messages={"required": "Onboarded VNF package info without VNF sw version"})
    vnfd_version = String(required=True, error_messages={"required": "Onboarded VNF package info without VNFD version"})
    checksum = String(required=True, error_messages={"required": "Onboarded VNF package info without checksum"})
    software_image = List(Nested(VnfPackageSoftwareImageInformationSerializer))
    additional_artifact = List(Nested(VnfPackageArtifactInformationSerializer))
    operational_state = String(choices=OperationalState.get_values())
    usage_state = String(choices=UsageState.get_values())
    deletion_pending = Boolean()
    user_defined_data = Dict(keys=String(), values=String())
    vnf_id = List(String())

    @pre_load
    def is_valid(self, data, **kwargs):
        if len(data.get('software_image', [])) == 0:
            raise ValidationError("Onboarded VNF package info without software images", "software_image")

        return data


class VduCpdSerializer(CpdSerializer):
    int_virtual_link_desc = String()
    bitrate_requirement = Integer()
    virtual_network_interface_requirements = List(Nested(VirtualNetworkInterfaceRequirementsSerializer))


class VduSerializer(Schema):
    vdu_id = String(required=True, error_messages={"required": "VDU without ID"})
    vdu_name = String(required=True, error_messages={"required": "VDU without name"})
    description = String(required=True, error_messages={"required": "VDU without description"})
    int_cpd = List(Nested(VduCpdSerializer))
    virtual_compute_desc = String(required=True, error_messages={"required": "VDU without virtual compute descriptor"})
    virtual_storage_desc = List(String())
    boot_order = Dict(keys=Integer(), values=String())
    sw_image_desc = Nested(SwImageDescSerializer)
    nfvi_constraint = List(String())
    monitoring_parameter = List(Nested(MonitoringParameterSerializer))

    @pre_load
    def is_valid(self, data, **kwargs):
        if len(data.get('int_cpd', [])) == 0:
            raise ValidationError("VDU without internal connection points", "int_cpd")

        return data


class VnfVirtualLinkDescSerializer(Schema):
    virtual_link_desc_id = String(required=True, error_messages={"required": "VNF VLD without ID"})
    connectivity_type = Nested(ConnectivityTypeSerializer, required=True,
                               error_messages={"required": "VNF VLD without connectivity type"})
    test_access = List(String())
    description = String()
    monitoring_parameter = List(Nested(MonitoringParameterSerializer))
    virtual_link_desc_flavour = List(Nested(VirtualLinkDfSerializer))

    @pre_load
    def is_valid(self, data, **kwargs):
        if len(data.get('virtual_link_desc_flavour', [])) == 0:
            raise ValidationError("VNF VLD without deployment flavour", "virtual_link_desc_flavour")

        return data


class VnfExtCpdSerializer(CpdSerializer):
    int_virtual_link_desc = String()
    int_cpd = String()
    virtual_network_interface_requirements = List(Nested(VirtualNetworkInterfaceRequirementsSerializer))

    @pre_load
    def is_valid(self, data, **kwargs):
        if data.get('int_virtual_link_desc') is None and data.get('int_cpd') is None:
            raise ValidationError("VNF external connection point without reference to internal VLD ID or CPD ID",
                                  "int_virtual_link_desc & int_cpd")

        return data


class VduProfileSerializer(Schema):
    vdu_id = String(required=True, error_messages={"required": "VDU profile without VDU ID"})
    min_number_of_instances = Integer()
    max_number_of_instances = Integer()
    local_affinity_or_anti_affinity_rule = List(Nested(AffinityRuleSerializer))
    affinity_or_anti_affinity_group_id = List(String())


class VduLevelSerializer(Schema):
    vdu_id = String(required=True, error_messages={"required": "VDU level without VDU ID"})
    number_of_instances = Integer()


class InstantiationLevelSerializer(Schema):
    level_id = String(required=True, error_messages={"required": "Instantiation level without ID"})
    description = String(required=True, error_messages={"required": "Instantiation level without description"})
    vdu_level = List(Nested(VduLevelSerializer))
    scale_info = List(Nested(ScaleInfoSerializer))

    @pre_load
    def is_valid(self, data, **kwargs):
        if len(data.get('vdu_level', [])) == 0:
            raise ValidationError("Instantiation level without VDU levels", "vdu_level")

        return data


class InstantiateVnfOpConfigSerializer(Schema):
    parameter = List(String())


class ScaleVnfOpConfigSerializer(Schema):
    parameter = List(String())
    scaling_by_more_than_one_step_supported = Boolean()


class ScaleVnfToLevelOpConfigSerializer(Schema):
    parameter = List(String())
    arbitrary_target_levels_supported = Boolean()


class ChangeVnfFlavourOpConfigSerializer(Schema):
    parameter = List(String())


class HealVnfOpConfigSerializer(Schema):
    parameter = List(String())
    cause = List(String())


class ChangeExtVnfConnectivityOpConfig(Schema):
    parameter = List(String())


class VnfLcmOperationsConfigurationSerializer(Schema):
    instantiate_vnf_op_config = Nested(InstantiateVnfOpConfigSerializer)
    scale_vnf_op_config = Nested(ScaleVnfOpConfigSerializer)
    scale_vnf_to_level_op_config = Nested(ScaleVnfToLevelOpConfigSerializer)
    change_vnf_flavour_op_config = Nested(ChangeVnfFlavourOpConfigSerializer)
    heal_vnf_op_config = Nested(HealVnfOpConfigSerializer)
    operate_vnf_op_config = Nested(TerminateVnfOpConfigSerializer)
    terminate_vnf_op_config = Nested(TerminateVnfOpConfigSerializer)
    change_ext_vnf_connectivity_op_config = Nested(ChangeExtVnfConnectivityOpConfig)


class ScalingAspectSerializer(Schema):
    sa_id = String(required=True, error_messages={"required": "Scaling aspect without ID"})
    sa_name = String(required=True, error_messages={"required": "Scaling aspect without name"})
    sa_description = String(required=True, error_messages={"required": "Scaling aspect without description"})
    associated_group = String()
    max_scale_level = Integer()


class VnfDfSerializer(Schema):
    flavour_id = String(required=True, error_messages={"required": "VNF DF without ID"})
    description = String(required=True, error_messages={"required": "VNF DF without description"})
    vdu_profile = List(Nested(VduProfileSerializer))
    virtual_link_profile = List(Nested(VirtualLinkProfileSerializer))
    instantiation_level = List(Nested(InstantiationLevelSerializer))
    default_instantiation_level_id = String()
    supported_operation = List(String(choices=VnfLcmOperation.get_values()))
    vnf_lcm_operations_configuration = Nested(VnfLcmOperationsConfigurationSerializer, required=True,
                                              error_messages={
                                                  "required": "VNF DF without VNF LCM operation configuration"})
    affinity_or_anti_affinity_group = List(Nested(AffinityOrAntiAffinityGroupSerializer))
    monitoring_parameter = List(Nested(MonitoringParameterSerializer))
    scaling_aspect = List(Nested(ScalingAspectSerializer))

    @pre_load
    def is_valid(self, data, **kwargs):
        if len(data.get('vdu_profile', [])) == 0:
            raise ValidationError("VNF DF without VDU profile", "vdu_profile")

        elif len(data.get('instantiation_level', [])) == 0:
            raise ValidationError("VNF DF without instantiation level", "instantiation_level")

        return data


class VnfConfigurablePropertiesSerializer(Schema):
    auto_scalable = Boolean(default=False)
    auto_healable = Boolean(default=False)
    additional_configurable_property = List(String())


class VnfInfoModifiableAttributesSerializer(Schema):
    extension = Dict(keys=String(), values=String())
    metadata_ifa = Dict(keys=String(), values=String())


class VnfdElementGroupSerializer(Schema):
    vnfd_element_group_id = String(required=True, error_messages={"required": "VNFD element group without ID"})
    description = String(required=True, error_messages={"required": "VNFD element group without descriptio"})
    vdu = List(String())
    virtual_link_desc = List(String())


class VnfIndicatorSerializer(Schema):
    indicator_id = String(required=True, error_messages={"required": "VNF indicator without ID"})
    name = String()
    indicator_value = String()
    source = String(choices=VnfIndicatorSource.get_values())


class VnfdSerializer(Schema):
    onboarded_vnf_pkg_info = Nested(OnboardedVnfPkgInfoSerializer)
    vnfd_id = String(required=True, error_messages={"required": "VNFD without VNFD ID"})
    vnf_provider = String(required=True, error_messages={"required": "VNFD without VNF provider"})
    vnf_product_name = String(required=True, error_messages={"required": "VNFD without VNF product name"})
    vnf_software_version = String(required=True, error_messages={"required": "VNFD without VNF sw version"})
    vnfd_version = String(required=True, error_messages={"required": "VNFD without VNFD version"})
    vnf_product_info_name = String()
    vnf_product_info_description = String()
    vnfm_info = List(String())
    localization_language = List(String())
    default_localization_language = String()
    vdu = List(Nested(VduSerializer))
    virtual_compute_desc = List(Nested(VirtualComputeDescSerializer))
    virtual_storage_desc = List(Nested(VirtualStorageDescSerializer))
    int_virtual_link_desc = List(Nested(VnfVirtualLinkDescSerializer))
    vnf_ext_cpd = List(Nested(VnfExtCpdSerializer))
    deployment_flavour = List(Nested(VnfDfSerializer))
    configurable_properties = Nested(VnfConfigurablePropertiesSerializer)
    modifiable_attributes = Nested(VnfInfoModifiableAttributesSerializer)
    life_cycle_management_script = List(Nested(LifeCycleManagementScriptSerializer))
    element_group = List(Nested(VnfdElementGroupSerializer))
    vnf_indicator = List(Nested(VnfIndicatorSerializer))


@pre_load
def is_valid(self, data, **kwargs):
    if len(data.get('vnfm_info', [])) == 0:
        raise ValidationError("VNFD without VNFM info", "vnfm_info")

    elif len(data.get('vdu', [])) == 0:
        raise ValidationError("VNFD without VDUs", "vdu")

    elif len(data.get('vnf_ext_cpd', [])) == 0:
        raise ValidationError("VNFD without external connection points", "vnf_ext_cpd")

    elif len(data.get('deployment_flavour', [])) == 0:
        raise ValidationError("VNFD without deployment flavours", "deployment_flavour")

    elif len(data.get('modifiable_attributes', [])) == 0:
        raise ValidationError("VNFD without modifiable attributes", "modifiable_attributes")
    return data
