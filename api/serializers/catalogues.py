from marshmallow import Schema, pre_load, ValidationError
from marshmallow.fields import String, Dict, Url, Nested, List, Date, Integer, Boolean

from api.enums.catalogues import OperationalState, UsageState
from api.enums.ns_descriptor import LayerProtocol, CpRole, AddressType, IpVersion


class OnBoardVnfPackageRequestSerializer(Schema):
    name = String(required=True, error_messages={"required": "On board VNF package request without name"})
    version = String(required=True, error_messages={"required": "On board VNF package request without version"})
    provider = String(required=True, error_messages={"required": "On board VNF package request without provider"})
    checksum = String(required=True, error_messages={"required": "On board VNF package request without checksum"})
    user_defined_data = Dict(keys=String(), values=String())
    vnf_package_path = Url(required=True,
                           error_messages={"required": "On board VNF package request without package path"})


class SoftwareImageInformation(String):
    software_image_id = String(required=True, error_messages={"required": "Sw image info without ID"})
    name = String(required=True, error_messages={"required": "Sw image info without name"})
    provider = String()
    version = String()
    checksum = String()
    container_format = String()
    disk_format = String()
    created_at = Date()
    min_disk = Integer()
    min_ram = Integer()
    size = Integer()
    user_metadata = Dict(keys=String(), values=String())


class VnfPackageSoftwareImageInformation(Schema):
    access_information = String(required=True,
                                error_messages={"required": "VNF package sw image info without access information"})
    software_image_information = Nested(SoftwareImageInformation, required=True, error_messages={
        "required": "VNF package sw image info without sw image information"})


class VnfPackageArtifactInformation(Schema):
    selector = String(required=True, error_messages={"required": "VNF package artifact information without selector"})
    metadata = String(required=True, error_messages={"required": "VNF package artifact information without metadata"})


class OnboardedVnfPkgInfo(Schema):
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
    software_image = List(Nested(VnfPackageSoftwareImageInformation))
    additional_artifact = List(Nested(VnfPackageArtifactInformation))
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


class AddressDataSerializer(Schema):
    address_type = String(choices=AddressType.get_values())
    ip_address_assignment = Boolean()
    floating_ip_activated = Boolean()
    management = Boolean()
    ip_address_type = String(choices=IpVersion.get_values())
    number_of_ip_address = Integer()


class VirtualNetworkInterfaceRequirements(Schema):
    name = String()
    description = String()
    support_mandatory = Boolean()
    net_requirement = String(required=True,
                             error_messages={"required": "Virtual network interface requirement without requirement"})
    nic_io_requirements = String()


class VduCpd(Schema):
    cpd_id = String(required=True, error_messages={"required": "CPD without ID"})
    layer_protocol = String(choices=LayerProtocol.get_values(), required=True,
                            error_messages={"required": "CPD without layer protocol"})
    cp_role = String(choices=CpRole.get_values())
    description = String()
    address_data = List(Nested(AddressDataSerializer))
    int_virtual_link_desc = String()
    bitrate_requirement = Integer()
    virtual_network_interface_requirements = List(Nested(VirtualNetworkInterfaceRequirements))


class SwImageDesc(Schema):
    sw_image_id = String(required=True, error_messages={"required": "Sw Image Descriptor without ID"})
    name = String(required=True, error_messages={"required": "Sw Image Descriptor without name"})
    version = String(required=True, error_messages={"required": "Sw Image Descriptor without version"})
    checksum = String(required=True, error_messages={"required": "Sw Image Descriptor without checksum"})
    container_format = String()
    disk_format = String()
    min_disk = Integer()
    min_ram = Integer()
    size = Integer()
    sw_image = String(required=True, error_messages={"required": "Sw Image Descriptor without sw image"})
    operating_system = String()
    supported_virtualization_environment = String()


class MonitoringParameter(Schema):
    monitoring_parameter_id = String(required=True, error_messages={"required": "Monitoring Parameter without ID"})
    name = String()
    performance_metric = String(required=True, error_messages={"required": "Monitoring Parameter without metric"})
    exporter = String()
    params = Dict(keys=String(), values=String())
    type = String()


class Vdu(Schema):
    vdu_id = String(required=True, error_messages={"required": "VDU without ID"})
    vdu_name = String(required=True, error_messages={"required": "VDU without name"})
    description = String(required=True, error_messages={"required": "VDU without description"})
    int_cpd = List(Nested(VduCpd))
    virtual_compute_desc = String(required=True, error_messages={"required": "VDU without virtual compute descriptor"})
    virtual_storage_desc = List(String())
    boot_order = Dict(keys=String(), values=String())
    sw_image_desc = Nested(SwImageDesc)
    nfvi_constraint = List(String())
    monitoring_parameter = List(Nested(MonitoringParameter))

    @pre_load
    def is_valid(self, data, **kwargs):
        if len(data.get('int_cpd', [])) == 0:
            raise ValidationError("VDU without internal connection points", "int_cpd")

        return data


class VirtualStorageDesc(Schema):
    storage_id = String(required=True, error_messages={"required": "Virtual storage descriptor without id"})
    type_of_storage = String(required=True, error_messages={"required": "Virtual storage descriptor without type"})
    size_of_storage = Integer()
    rdma_enabled = Boolean()
    sw_image_desc = String()


class AppExternalCpd(Schema):
    virtual_network_interface_requirements = List(Nested(VirtualNetworkInterfaceRequirements))


class Appd(Schema):
    appD_id = String()
    app_name = String()
    app_provider = String()
    app_soft_version = String()
    appD_version = String()
    mec_version = List(String())
    app_info_name = String()
    app_description = String()
    sw_image_descriptor = Nested(SwImageDesc)
    virtual_storage_descriptor = List(Nested(VirtualStorageDesc))
    app_ext_cpd = List(Nested(AppExternalCpd))


class VirtualComputeDesc(Schema):
    appd = Nested(Appd)


class Vnfd(Schema):
    onboarded_vnf_pkg_info = Nested(OnboardedVnfPkgInfo)
    vnfd_id = String()
    vnf_provider = String()
    vnf_product_name = String()
    vnf_software_version = String()
    vnfd_version = String()
    vnf_product_info_name = String()
    vnf_product_info_description = String()
    vnfm_info = List(String())
    localization_language = List(String())
    default_localization_language = String()
    vdu = List(Nested(Vdu))
    virtual_compute_desc = List(Nested(VirtualComputeDesc))
