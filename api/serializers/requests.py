from marshmallow import Schema
from marshmallow.fields import String, List, Nested
from serializers.descriptors import NsdSerializer
from serializers.vs_blueprint import VsdNsdTranslationRuleSerializer, VsBlueprintSerializer
from serializers.catalogues import OnBoardVnfPackageRequestSerializer


class VsBlueprintRequestSerializer(Schema):
    ndsd = List(Nested(NsdSerializer))
    translation_rules = List(Nested(VsdNsdTranslationRuleSerializer))
    vs_blueprint = Nested(VsBlueprintSerializer, required=True,
                          error_messages={"required": "Onboard VS blueprint request without VS blueprint"})
    # TODO: List<NST> nsts
    vnfPackages = List(Nested(OnBoardVnfPackageRequestSerializer))
    owner = String()
