from werkzeug.exceptions import HTTPException
from api.serializers.vs_descriptor import VsDescriptorSerializer
from api.serializers.vs_blueprint import VsBlueprintInfoSerializer
from api.serializers.ns_template import NstSerializer
from api.models.ns_template import Nst
from api.queries.vs_descriptor import get_vs_descriptors
from api.queries.vs_blueprint import get_vs_blueprints


def get_info(content):
    if content.get("msgType") == "createVSI" and (vsi_id := content.get('vsiId')) is not None:
        tenant_id, data = content.get('tenantId'), content.get('data')
        vsd_id = data.get('vsdId')

        requested_data = {'message': 'Success', 'vsiId': vsi_id, 'msgType': 'catalogueInfo', 'error': False, 'data': {}}

        try:
            vsd = VsDescriptorSerializer().dump(get_vs_descriptors(vsd_id=vsd_id, tenant_id=tenant_id)[0])

            vsb_id = vsd.get('vs_blueprint_id')
            vsbi = VsBlueprintInfoSerializer().dump(
                get_vs_blueprints(vsb_id=vsb_id, tenant_id=tenant_id, with_translation_rules=True)[0])

            nsts_id = [rule.get('nst_id') for rule in vsbi.get('vs_blueprint', {}).get('translation_rules', [])]
            nsts = NstSerializer(many=True).dump(Nst.objects.filter(nst_id__in=nsts_id))

            requested_data['data'] = {
                'vsd': vsd,
                'vs_blueprint_info': vsbi,
                'nsts': nsts
            }
        except HTTPException as e:
            requested_data['message'] = e.get_description()
            requested_data['error'] = True

        except Exception:
            requested_data['message'] = "Internal Error"
            requested_data['error'] = True

        return requested_data
