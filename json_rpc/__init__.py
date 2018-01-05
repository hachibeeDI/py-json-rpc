# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import


from uuid import uuid4
from functools import wraps
from typing import (
    Dict,
    List,
    Union,
    Optional,
    Any,
)


from .variants import JSON_RPC_VERSION, ErrorCode
from .error import create_error_response, code_to_response

RPC_STACK = {}


def register(target):
    """
    Decorator to register functions as Remote procedure.

    In default, rpc method name will be the name of function.
    First argument would be a name of the method.

    Example:

    >>> @register
    ... def func_x(a, b, c):
    ...     pass
    ...

    >>> @register('named')
    ... def func_named(a, b, c):
    ...     pass
    ...
    """

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


def _call(id, name, params: Union[List, Dict]) -> Dict:
    """
    JSON-RPC supports positional arguments and named arguments.
    """
    from inspect import signature

    if name not in RPC_STACK:
        return code_to_response(id, ErrorCode.METHOD_NOT_FOUND)

    function = RPC_STACK[name]
    parameter_spec = signature(function).parameters

    result = None
    if isinstance(params, List):
        if len(params) != len(parameter_spec):
            return code_to_response(id, ErrorCode.INVALID_PARAMS)

        result = function(*params)

    elif isinstance(params, Dict):
        if set(params.keys()) != set(parameter_spec.keys()):
            return code_to_response(id, ErrorCode.INVALID_PARAMS)

        result = function(**params)

    else:
        return code_to_response(id, ErrorCode.INVALID_REQUEST)

    # notification request has no id
    if id is None:
        return None

    return {
        'jsonrpc': JSON_RPC_VERSION,
        'result': result,
        'id': id,
    }


def _eval(jsonrpc, method, id=None, params=None):
    if params is None:
        params = []

    try:
        return _call(id, method, params)
    except Exception as e:
        return code_to_response(id, ErrorCode.UNEXPECTED_ERROR, str(e))


def rpc_dispatcher(request: Union[List, Dict]):
    """
    Dispatcher for rpc request.
    Receive a JSON-rpc request then returns a result.
    The request must be follows JSON-rpc protocol.  Basically a dict but it can be a list if it is batch.
    """

    if isinstance(request, List):
        return list(filter(None, [_eval(**r) for r in request]))
    elif isinstance(request, Dict):
        return _eval(**request)
    else:
        assert False, 'Invalid request'


def make_request(method: str, params: Union[List, Dict[str, Any]], request_id: Optional[str]=None):
    """
    Helper function to create a request follows JSON-rpc protocol.

    >>> make_request('aa', {"aa": "rpc"}, '111')
    {"jsonrpc": "2.0", "method": "aa", "params": {"aa": "rpc"}, "id": "111"}
    """

    if not request_id:
        request_id = str(uuid4())
    return {
        'jsonrpc': JSON_RPC_VERSION,
        'params': params,
        'method': method,
        'id': request_id,
    }
