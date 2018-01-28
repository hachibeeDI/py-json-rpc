[![CircleCI](https://circleci.com/gh/hachibeeDI/py-json-rpc.svg?style=svg)](https://circleci.com/gh/hachibeeDI/py-json-rpc)

# PY-JSON-RPC

Simple and Pluggable JSON RPC toolkit to declare procedures super easy like Flask.

PY-JSON-RPC supports async function handling!!  It could improve your batch call performance.


## Install

```sh
$ pip install py-json-rpc
```


## Sample


### None async

Tornado is not a required.  Just an sample to create HTTP handler.  You can use other HTTP handling solution Flask, Django... if you would like to.

```python

import json

import requests
import tornado.ioloop
import tornado.web

from json_rpc import register, rpc_dispatcher, make_request
from json_rpc.server.http import create_handler


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
        'id': '111',
    })
    rpc2 = rpc_dispatcher(make_request('test/hyoe', {'x': 20, 'y': 10}))
    print(json.dumps(rpc))
    # => {"jsonrpc": "2.0", "result": "cccc  called", "id": "111"}
    print(json.dumps(rpc))
    # => u'{"jsonrpc": "2.0", "result": "cccc  called", "id": "some_uuid_for_you"}'

    # there is HTTP server to receive rpc call
    def make_app():
        return tornado.web.Application([
            (r'/rpc', create_handler(tornado.web.RequestHandler)),
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


### Async


```python

loop = asyncio.get_event_loop()
app = Registrator(loop=loop)


@app.register
async def plus_rpc(x, y):
    return x + y


@app.register
async def minus(x, y):
    return x - y


@app.register
async def heavy_request(a):
    print(f'start heavy request... {a}sec')
    await asyncio.sleep(a)
    print('end heavy request...')
    return 'home page!'


"""
No difference with none async version to call those functions.
More samples in test code.  Document is under writing...
"""


def test_plain():
    """
    The func is going to be async as it was if it was called normally.
    """
    result = asyncio.ensure_future(plus_rpc(1, 2))
    result = loop.run_until_complete(result)
    assert result == 3, result


def test_positional_rpc_call():
    rpc_result = app.dispatch({
        'jsonrpc': '2.0',
        'method': 'plus_rpc',
        'params': [1, 2],
        'id': 111,
    })
    assert rpc_result.get('result') == 3, rpc_result

```


### Integrate with Tornado

You can see `from json_rpc.server.http import create_handler` and the usage in the example on above.  A function `create_handler` will create a handler instance for Tornado.
Please be aware that the instance haven't implement any security functionality.  In case you'd like to a RPC end point to be public, you might want to consider create a handler by yourself (or feel free to open an issue ...or PR of course!).


### Integrate with Flask

Small sample

```python
import json

from flask import Flask, request
from json_rpc import register, rpc_dispatcher


app = Flask(__name__)


@register
def hoge(name):
    return f'{name} called'


@app.route('/', methods=['POST'])
def hello():
    result = rpc_dispatcher(request.json)
    return json.dumps(result)
```

To test:

```python
>>> print(requests.post('http://localhost:5000', json=make_request('hoge', ['cccc'])).text)
```


### Integrate with Django

See Flask.  View can be integrate with this module easily.


## Fully supports JSON RPC protocol

List argument, named argument, notify, batch request and proper error codes.


## Supported Python versions

Greater than or equal to Python 3.6


## Road Map

- Security instruction

- WebSocket sample

- MQTT server or GNATS daemon sample
