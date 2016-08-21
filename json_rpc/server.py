# -*- coding: utf-8 -*-

import json

import tornado.ioloop
import tornado.web

from . import rpc_dispatcher


class RPCHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')

    def get(self):
        self.write('rpc demo')

    def post(self):
        rpc_request = json.loads(self.request.body)
        if isinstance(rpc_request, list):
            result = [rpc_dispatcher(**r) for r in rpc_request]
        else:
            result = [rpc_dispatcher(**rpc_request)]
        self.write(json.dumps(result))
