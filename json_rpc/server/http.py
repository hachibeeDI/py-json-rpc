# -*- coding: utf-8 -*-

import json

from tornado.web import RequestHandler

from .. import rpc_dispatcher


class RPCHandler(RequestHandler):

    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')

    def get(self):
        self.write('rpc demo')

    def post(self):
        rpc_request = json.loads(self.request.body)
        result = rpc_dispatcher(rpc_request)

        self.write(json.dumps(result))
