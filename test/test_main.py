# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals,)

import json
import unittest

from nose.tools import eq_


from json_rpc import register, rpc_dispatcher, make_request
from json_rpc.server import RPCHandler


suite = unittest.TestSuite()
loader = unittest.TestLoader()
# use `nosetests --with-doctest`
# suite.addTests(doctest.DocTestSuite(letexpr))


# define method very easy
@register
def identity(aa):
    return aa + ' called'


# you can appoint method name for rpc call
@register('plus')
def plus(x, y):
    return x + y


def test_plain():
    result = plus(1, 2)
    assert result == 3


def test_positional_rpc_call():
    rpc_result = rpc_dispatcher(**{
        'jsonrpc': '2.0',
        'method': 'plus',
        'params': [1, 2],
        'id': 111,
    })
    assert rpc_result['result'] == 3


def test_named_rpc_call():
    rpc_result = rpc_dispatcher(**{
        'jsonrpc': '2.0',
        'method': 'plus',
        'params': {'x': 1, 'y': 2},
        'id': 111,
    })
    assert rpc_result['result'] == 3
