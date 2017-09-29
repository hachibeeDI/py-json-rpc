# -*- coding: utf-8 -*-

import json

from tornado.websocket import WebSocketHandler

from .. import rpc_dispatcher


class RPCHandler(WebSocketHandler):
    def open(self):
        pass

    def on_message(self, message):
        rpc_request = json.loads(message)
        result = rpc_dispatcher(rpc_request)
        self.write_message(json.dumps(result))

    def on_close(self):
        pass
