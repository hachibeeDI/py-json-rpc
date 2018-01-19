from .variants import JSON_RPC_VERSION, ErrorCode, Fail


CODE_TO_MESSAGE = {
    ErrorCode.PARSE_ERROR: 'Parse error Invalid JSON was received by the server.  An error occurred on the server while parsing the JSON text.',
    ErrorCode.INVALID_REQUEST: 'The JSON sent is not a valid Request object.',
    ErrorCode.METHOD_NOT_FOUND: 'The method does not exist / is not available.',
    ErrorCode.INVALID_PARAMS: 'Invalid method parameter(s).',
    ErrorCode.INTERNAL_ERROR: 'Internal JSON-RPC error.',
    ErrorCode.UNEXPECTED_ERROR: 'unexpected error is occurred',
}


def create_error_response(id, code, message):
    return {
        'jsonrpc': JSON_RPC_VERSION,
        'error': {
            'code': code,
            'message': message,
        },
        'id': id,
    }


def code_to_response(id, code, message=''):
    defined_message = CODE_TO_MESSAGE[code]
    return create_error_response(id, code, f'{defined_message}. {message}')


def as_failed(id, code, message=''):
    return Fail(id, code, message)
