from werkzeug.exceptions import HTTPException
from rabbitmq.adaptor import Messaging
from threading import Thread
from api.serializers.vs_descriptor import VsDescriptorSerializer
from api.serializers.vs_blueprint import VsBlueprintInfoSerializer
from api.queries.vs_descriptor import get_vs_descriptors
from api.queries.vs_blueprint import get_vs_blueprints
import json


class MessageReceiver(Thread):

    def __init__(self):
        super().__init__()
        self.messaging = Messaging()
        self.messaging.consumeExchange("vsLCM_Management", self.callback)

    def _nested_blueprint_in_descriptor(self, vsd_id, tenant_id="tenant"):
        descriptor_data = VsDescriptorSerializer().dump(get_vs_descriptors(vsd_id=vsd_id, tenant_id=tenant_id)[0])

        vs_blueprint_id = descriptor_data.get('vs_blueprint_id', None)
        vs_blueprint_info_data = VsBlueprintInfoSerializer().dump(
            get_vs_blueprints(vsb_id=vs_blueprint_id, with_translation_rules=True)[0])

        return descriptor_data, vs_blueprint_info_data

    def callback(self, ch, method, properties, body):
        print(" [x] Received status update %r" % body)
        content = json.loads(body)

        if (vsi_id := content.get('vsiId')) is None:
            return

        if False:  # Dummy response
            with open('rabbitmq/good_response.json') as f:
                requested_data = json.load(f)
            self.messaging.publish2Queue(f"vsLCM_{vsi_id}", json.dumps(requested_data))
            return

        if content.get("msgType") == "createVSI":
            data = content.get('data')
            vsd_id, vssis = data.get('vsdId'), data.get('vssis', [])

            requested_data = {'message': 'Success', 'error': False, 'data': {}}

            # Need the tenant_id
            try:
                vsd, vs_blueprint_info = self._nested_blueprint_in_descriptor(vsd_id)
                nested_vssis = []
                for vssi in vssis:
                    nested_vsd, nested_vs_blueprint_info = self._nested_blueprint_in_descriptor(
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

            self.messaging.publish2Queue(f"vsLCM_{vsi_id}", json.dumps(requested_data))

            # with open('rabbitmq/good_response.json', 'w') as f:
            #     json.dump(requested_data, f)

    def run(self):
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.messaging.startConsuming()
