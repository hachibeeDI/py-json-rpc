[![CircleCI](https://circleci.com/gh/hachibeeDI/py-json-rpc.svg?style=svg)](https://circleci.com/gh/hachibeeDI/py-json-rpc)

# PY-JSON-RPC

JSON RPC toolkit to declare procedures super easy like Flask.


## Example

```python

import json

import requests
import tornado.ioloop
import tornado.web

from json_rpc import register, rpc_dispatcher, make_request
from json_rpc.server import RPCHandler

# Basic usage to define a function which supports JSON RPC protocol.
@register
def aa(aa):
    return aa + ' called'


# You can name for RPC function if you need it.
@register('test/hyoe')
def hoge(x, y):
    return x + y


if __name__ == '__main__':
    # You can call functions as normal.
    print(aa(aa='cc'))
    # => 'cc called'

    # You can call the function via Json RPC protocol.
    rpc = rpc_dispatcher({
        'jsonrpc': '2.0',
        'method': 'aa',
        'params': {'aa': 'rpc'},
        'id': 111,
    })
    # make_request is a helper to create a request call.
    rpc2 = rpc_dispatcher(make_request('test/hyoe', {'x': 20, 'y': 10}))
    print(json.dumps(rpc))
    # => {"jsonrpc": "2.0", "result": "cccc  called", "id": "111"}
    print(json.dumps(rpc))
    # => u'{"jsonrpc": "2.0", "result": "cccc  called", "id": "some_uuid_for_you"}'

    # This module has a handler to create HTTP server (we only supports tornado so far) supports JSON RPC super easy.
    def make_app():
        return tornado.web.Application([
            (r'/rpc', RPCHandler),
        ])
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


    """
    example to make rpc request
    """
    print(requests.post('http://localhost:8888/rpc', data=json.dumps(make_request('aa', {'aa': 'cccc '}))).text)
    # => {"jsonrpc": "2.0", "result": "cccc  called", "id": "some_uuid_for_you"}
    print(requests.post('http://localhost:8888/rpc', data=json.dumps(make_request('test/hyoe', {'x': 3, 'y': 3}))).text)
    # => "jsonrpc": "2.0", "result": 6, "id": "cff9667f-a520-42cf-9216-ef2fa051a213"}
```


## Fully supports JSON RPC protocol

List argument, named argument, notify, batch request and proper error codes.


## Supported Python versions

Greater than or equal to Python 3.6


## Road Map

- WebSocket

- MQTT server
