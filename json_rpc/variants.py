from enum import Enum


JSON_RPC_VERSION = '2.0'


class ErrorCode(Enum):

    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603
    """
    Reserved for implementation-defined server-errors.
    Server error = -32000 to -32099
    """

    # error for application specific error which is unexpected
    UNEXPECTED_ERROR = -32099


    CODE_TO_MESSAGE = {
        PARSE_ERROR: 'Parse error Invalid JSON was received by the server.  An error occurred on the server while parsing the JSON text.',
        INVALID_REQUEST: 'The JSON sent is not a valid Request object.',
        METHOD_NOT_FOUND: 'The method does not exist / is not available.',
        INVALID_PARAMS: 'Invalid method parameter(s).',
        INTERNAL_ERROR: 'Internal JSON-RPC error.',
        UNEXPECTED_ERROR: 'unexpected error is occurred',
    }
