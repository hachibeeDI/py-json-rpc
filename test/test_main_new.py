# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals,)

import unittest

from nose.tools import eq_

from json_rpc import make_request, Registrator
from json_rpc.server.http import create_handler


suite = unittest.TestSuite()
loader = unittest.TestLoader()
# use `nosetests --with-doctest`
# suite.addTests(doctest.DocTestSuite(letexpr))

app = Registrator()


@app.register
def plus_rpc(x, y):
    return x + y


def test_plain():
    result = plus_rpc(1, 2)
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
