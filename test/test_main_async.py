# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals,)

import unittest
import asyncio
from time import time

from nose.tools import eq_

from json_rpc import make_request, Registrator
from json_rpc.variants import ErrorCode
from json_rpc.server.http import create_handler


suite = unittest.TestSuite()
loader = unittest.TestLoader()
# use `nosetests --with-doctest`
# suite.addTests(doctest.DocTestSuite(letexpr))


loop = asyncio.get_event_loop()
app = Registrator(loop=loop)


@app.register
async def plus_rpc(x, y):
    # await asyncio.sleep(0.3)
    return x + y


@app.register
async def minus(x, y):
    # await asyncio.sleep(0.3)
    return x - y


@app.register
async def will_failed_func(x):
    raise ValueError(x)


@app.register
async def heavy_request(a):
    print(f'start heavy request... {a}sec')
    await asyncio.sleep(a)
    print('end heavy request...')
    return 'home page!'


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


def test_named_rpc_call():
    rpc_result = app.dispatch({
        'jsonrpc': '2.0',
        'method': 'plus_rpc',
        'params': {'x': 1, 'y': 2},
        'id': 111,
    })
    assert rpc_result.get('result') == 3, rpc_result


def test_multiple():
    req1 = {
        'jsonrpc': '2.0',
        'method': 'plus_rpc',
        'params': [1, 2],
        'id': 111,
    }
    req2 = {
        'jsonrpc': '2.0',
        'method': 'plus_rpc',
        'params': [10, 20],
        'id': 111,
    }
    rpc_result = app.dispatch([req1, req2])
    assert rpc_result[0].get('result') == 3, rpc_result
    assert rpc_result[1].get('result') == 30, rpc_result


def test_notify():
    rpc_result = app.dispatch({
        'jsonrpc': '2.0',
        'method': 'plus_rpc',
        'params': {'x': 1, 'y': 2},
    })
    assert rpc_result is None, rpc_result


def test_notify_multiple():
    req1 = {
        'jsonrpc': '2.0',
        'method': 'plus_rpc',
        'params': [1, 2],
        'id': 111,
    }
    req2 = {
        'jsonrpc': '2.0',
        'method': 'plus_rpc',
        'params': [10, 20],
    }
    rpc_result = app.dispatch([req1, req2])

    assert len(rpc_result) == 1, rpc_result
    assert rpc_result[0].get('result') == 3, rpc_result


def test_make_request_named_arg():
    created_request = make_request('test_created', {'x': 1, 'y': 2})
    assert created_request['jsonrpc'] == '2.0'
    assert created_request['method'] == 'test_created'
    assert created_request['params'] == {'x': 1, 'y': 2}
    # generated id is random so cannot test that


def test_make_request_positional_arg():
    created_request = make_request('test_created_positional', ['first', 'second', 'third'])
    assert created_request['jsonrpc'] == '2.0'
    assert created_request['method'] == 'test_created_positional'
    assert created_request['params'] == ['first', 'second', 'third']
    # generated id is random so cannot test that


def test_failed_async_call():
    rpc_result = app.dispatch({
        'jsonrpc': '2.0',
        'method': 'will_failed_func',
        'params': ['hogeeeee'],
        'id': 666,
    })
    assert 'error' in rpc_result, rpc_result
    assert rpc_result['error']['code'] == ErrorCode.UNEXPECTED_ERROR, rpc_result


def test_concurrent():
    req1 = make_request('heavy_request', [1])
    req2 = make_request('heavy_request', [1])
    req3 = make_request('heavy_request', [1])

    start = time()
    rpc_result = app.dispatch([req1, req2, req3])
    time_took = time() - start

    assert rpc_result[0].get('result') == 'home page!', rpc_result
    assert time_took < 1.5, time_took
