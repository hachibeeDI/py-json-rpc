import json

from .. import rpc_dispatcher


def create_handler(klass):

    class RPCHandler(klass):

        def set_default_headers(self):
            self.set_header('Content-Type', 'application/json')

        def get(self):
            self.write('rpc demo')

        def post(self):
            rpc_request = json.loads(self.request.body)
            result = rpc_dispatcher(rpc_request)

            self.write(json.dumps(result))

    return RPCHandler
