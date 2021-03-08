from rest_framework_mongoengine.serializers import DocumentSerializer
from models.vs_blueprint import VsBlueprintInfo, VsBlueprint


class VsBlueprintSerializer(DocumentSerializer):
    class Meta:
        model = VsBlueprint


class VsBlueprintInfoSerializer(DocumentSerializer):
    vs_blueprint = VsBlueprintSerializer(many=False)

    class Meta:
        model = VsBlueprintInfo
