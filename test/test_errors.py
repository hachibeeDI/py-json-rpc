from json_rpc import register, rpc_dispatcher, make_request
from json_rpc.variants import ErrorCode


@register
def identity(aa):
    return aa + ' called'


@register
def erraiser():
    raise ValueError('hogeee')


def test_undef_method():
    rpc_result = rpc_dispatcher({
        'jsonrpc': '2.0',
        'method': 'gyoeee',
        'params': {'x': 1, 'y': 2},
        'id': 111,
    })

    assert 'error' in rpc_result, rpc_result

    error = rpc_result['error']
    assert error['code'] == ErrorCode.METHOD_NOT_FOUND, rpc_result


def test_invalid_pram():
    rpc_result = rpc_dispatcher({
        'jsonrpc': '2.0',
        'method': 'identity',
        'params': {'z': 'failed'},
        'id': 111,
    })

    assert 'error' in rpc_result, rpc_result

    error = rpc_result['error']
    assert error['code'] == ErrorCode.INVALID_PARAMS, rpc_result


def test_application_error():
    rpc_result = rpc_dispatcher({
        'jsonrpc': '2.0',
        'method': 'erraiser',
        'id': 111,
    })

    assert 'error' in rpc_result, rpc_result

    error = rpc_result['error']
    assert error['code'] == ErrorCode.UNEXPECTED_ERROR, rpc_result


def test_batch_contains_error():
    correct_result = {
        'jsonrpc': '2.0',
        'method': 'identity',
        'params': ['rpc'],
        'id': 111,
    }
    invalid_result = {
        'jsonrpc': '2.0',
        'method': 'erraiser',
        'id': 111,
    }
    rpc_result = rpc_dispatcher([correct_result, invalid_result])

    assert 'result' in rpc_result[0], rpc_result
    assert 'error' in rpc_result[1], rpc_result

    error = rpc_result[1]['error']
    assert error['code'] == ErrorCode.UNEXPECTED_ERROR, rpc_result
