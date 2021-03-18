from marshmallow import Schema
from marshmallow.fields import String, Dict


class OnBoardVnfPackageRequestSerializer(Schema):
    name = String(required=True, error_messages={"required": "On board VNF package request without name"})
    version = String(required=True, error_messages={"required": "On board VNF package request without version"})
    provider = String(required=True, error_messages={"required": "On board VNF package request without provider"})
    checksum = String(required=True, error_messages={"required": "On board VNF package request without checksum"})
    user_defined_data = Dict(keys=String(), values=String())
    vnf_package_path = String(required=True,
                              error_messages={"required": "On board VNF package request without package path"})
