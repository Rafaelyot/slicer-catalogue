from rabbitmq.adaptor import Messaging
from rabbitmq.api_wrapper import get_info
from threading import Thread

import json


class MessageReceiver(Thread):

    def __init__(self):
        super().__init__()
        self.messaging = Messaging()
        self.messaging.consumeExchange("vsLCM_Management", self.callback)

    def callback(self, ch, method, properties, body):
        print(" [x] Received status update %r" % body)
        content = json.loads(body)

        if (vsi_id := content.get('vsiId')) is None:
            return

        self.messaging.publish2Queue(f"vsLCM_{vsi_id}", json.dumps(get_info(content)))

    def run(self):
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.messaging.startConsuming()
