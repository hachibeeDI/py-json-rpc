# PY-JSON-RPC

JSON RPC toolkit to make server easily like Flask.


## Example

```python

import json

import requests
import tornado.ioloop
import tornado.web

from json_rpc import register, rpc_dispatcher, make_request
from json_rpc.server import RPCHandler

# define method very easy
@register
def aa(aa):
    return aa + ' called'


# you can appoint method name for rpc call
@register('test/hyoe')
def hoge(x, y):
    return x + y


if __name__ == '__main__':
    # you can call functions simply
    print(aa(aa='cc'))
    # => 'cc called'

    # you can call function via json rpc protocol
    rpc = rpc_dispatcher({
        'jsonrpc': '2.0',
        'method': 'aa',
        'params': {'aa': 'rpc'},
        'id': 111,
    })
    rpc2 = rpc_dispatcher(make_request('test/hyoe', {'x': 20, 'y': 10}))
    print(json.dumps(rpc))
    # => {"jsonrpc": "2.0", "result": "cccc  called", "id": "111"}
    print(json.dumps(rpc))
    # => u'{"jsonrpc": "2.0", "result": "cccc  called", "id": "some_uuid_for_you"}'

    # there is HTTP server to receive rpc call
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


## Support version

Greater than or equal to Python 3.6



## Road Map

- WebSocket

- MQTT server
