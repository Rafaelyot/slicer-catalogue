from marshmallow import Schema
from marshmallow.fields import String, List, Nested
from api.serializers.ns_descriptor import NsdSerializer
from api.serializers.ns_template import NstSerializer
from api.serializers.vs_blueprint import VsdNsdTranslationRuleSerializer, VsBlueprintSerializer
from api.serializers.catalogues import OnBoardVnfPackageRequestSerializer


class VsBlueprintRequestSerializer(Schema):
    nsds = List(Nested(NsdSerializer))
    translation_rules = List(Nested(VsdNsdTranslationRuleSerializer))
    nsts = List(Nested(NstSerializer))
    owner = String()
    vs_blueprint = Nested(VsBlueprintSerializer, required=True,
                          error_messages={"required": "Onboard VS blueprint request without VS blueprint"})
    vnf_packages = List(Nested(OnBoardVnfPackageRequestSerializer))




