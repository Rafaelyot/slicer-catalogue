from werkzeug.exceptions import HTTPException
from api.serializers.vs_descriptor import VsDescriptorSerializer
from api.serializers.vs_blueprint import VsBlueprintInfoSerializer
from api.queries.vs_descriptor import get_vs_descriptors
from api.queries.vs_blueprint import get_vs_blueprints


def _nested_blueprint_in_descriptor(vsd_id, tenant_id):
    descriptor_data = VsDescriptorSerializer().dump(get_vs_descriptors(vsd_id=vsd_id, tenant_id=tenant_id)[0])

    vs_blueprint_id = descriptor_data.get('vs_blueprint_id', None)
    vs_blueprint_info_data = VsBlueprintInfoSerializer().dump(
        get_vs_blueprints(vsb_id=vs_blueprint_id, with_translation_rules=True)[0])

    return descriptor_data, vs_blueprint_info_data


def get_info(content):
    if content.get("msgType") == "createVSI":
        data = content.get('data')
        vsd_id, vssis = data.get('vsdId'), data.get('vssis', [])

        requested_data = {'message': 'Success', 'error': False, 'vsdId': vsd_id, 'data': {}}

        # Need the tenant_id
        tenant_id = "tenant"
        try:
            vsd = VsDescriptorSerializer().dump(get_vs_descriptors(vsd_id=vsd_id, tenant_id=tenant_id)[0])
            vsbi = None

            requested_data['data'] = {
                'vsd': vsd,
                'vs_blueprint_info': vsbi
            }
        except HTTPException as e:
            requested_data['message'] = e.get_description()
            requested_data['error'] = True

        except Exception:
            requested_data['message'] = "Internal Error"
            requested_data['error'] = True

        print(requested_data)

        """
        try:
            vsd, vs_blueprint_info = _nested_blueprint_in_descriptor(vsd_id)
            nested_vssis = []
            for vssi in vssis:
                nested_vsd, nested_vs_blueprint_info = _nested_blueprint_in_descriptor(
                    vssi.get('descriptor_id'))
                nested_vssis.append({
                    'vsd': nested_vsd,
                    'vs_blueprint_info': nested_vs_blueprint_info
                })

            requested_data['data'] = {
                'vsd': vsd,
                'vs_blueprint_info': vs_blueprint_info,
                'vssis': nested_vssis
            }
        except HTTPException as e:
            requested_data['message'] = e.get_description()
            requested_data['error'] = True

        except Exception:
            requested_data['message'] = "Internal Error"
            requested_data['error'] = True
        """

    return requested_data
