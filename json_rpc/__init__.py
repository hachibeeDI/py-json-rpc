# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import


from uuid import uuid4
from functools import wraps


JSON_RPC_VERSION = '2.0'

RPC_STACK = {}


def register(target):
    if isinstance(target, str):
        # call as decorator with argument
        def decorate(func):

            @wraps(func)
            def __inner(*args, **kw):
                return func(*args, **kw)

            RPC_STACK[target] = __inner
            return __inner

        return decorate

    else:

        # call as normal decorator
        func = target

        @wraps(func)
        def __inner(*args, **kw):
            return func(*args, **kw)

        RPC_STACK[func.__name__] = __inner
        return __inner


def _call(name, params):
    """
    JSON-RPC supports positional arguments and named arguments.
    """
    if isinstance(params, (list, tuple)):
        return RPC_STACK[name](*params)
    elif isinstance(params, dict):
        return RPC_STACK[name](**params)


def _rpc_error(id, code, message):
    return {
        'jsonrpc': JSON_RPC_VERSION,
        'error': {
            'code': code,
            'message': message,
        },
        'id': id,
    }


def rpc_dispatcher(jsonrpc, method, params, id):
    if method not in RPC_STACK:
        return _rpc_error(id, 'NameError', "name '{}' is not defined".format(method))

    try:
        result = _call(method, params)
    except Exception as e:
        return _rpc_error(id, e.__class__.__name__, e.message)

    else:
        return {
            'jsonrpc': JSON_RPC_VERSION,
            'result': result,
            'id': id,
        }


def make_request(method, params):
    """
    e.g. {"jsonrpc": "2.0", "method": "aa", "params": {"aa": "rpc"}, "id": 111}
    """
    return {
        'jsonrpc': JSON_RPC_VERSION,
        'params': params,
        'method': method,
        'id': str(uuid4()),
    }
