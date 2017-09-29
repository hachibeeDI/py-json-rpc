# -*- coding: utf-8 -*-

import json

import tornado.ioloop
import tornado.web
from tornado.websocket import WebSocketHandler

from . import rpc_dispatcher


class RPCHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')

    def get(self):
        self.write('rpc demo')

    def post(self):
        rpc_request = json.loads(self.request.body)
        result = rpc_dispatcher(rpc_request)

        self.write(json.dumps(result))


class WebSocketHandler(WebSocketHandler):
    def open(self):
        pass

    def on_message(self, message):
        rpc_request = json.loads(message)
        result = rpc_dispatcher(rpc_request)
        self.write_message(json.dumps(result))

    def on_close(self):
        pass
