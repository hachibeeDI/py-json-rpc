from asyncio import iscoroutine
from enum import Enum


JSON_RPC_VERSION = '2.0'


class ErrorCode(Enum):
    """
    An enum object is having error definitions which was defined by the protocol.

    .. seealso::
        http://www.jsonrpc.org/specification#error_object

    .. csv-table::
        :header: code, message, meaning

        -32700, Parse error, Invalid JSON was received by the server.  An error occurred on the server while parsing the JSON text.
        -32600, Invalid Request, The JSON sent is not a valid Request object.
        -32601, Method not found, The method does not exist / is not available.
        -32602, Invalid params, Invalid method parameter(s).
        -32603, Internal error, Internal JSON-RPC error.
        -32000 to -32099, Server error, Reserved for implementation-defined server-errors.
    """

    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603

    # TODO: Reserved for implementation-defined server-errors.
    #   Server error = -32000 to -32099

    UNEXPECTED_ERROR = -32099
    """error for application specific error which is unexpected"""


CODE_TO_MESSAGE = {
    ErrorCode.PARSE_ERROR: 'Parse error Invalid JSON was received by the server.  An error occurred on the server while parsing the JSON text.',
    ErrorCode.INVALID_REQUEST: 'The JSON sent is not a valid Request object.',
    ErrorCode.METHOD_NOT_FOUND: 'The method does not exist / is not available.',
    ErrorCode.INVALID_PARAMS: 'Invalid method parameter(s).',
    ErrorCode.INTERNAL_ERROR: 'Internal JSON-RPC error.',
    ErrorCode.UNEXPECTED_ERROR: 'unexpected error is occurred',
}


class Fail:
    def __init__(self, id, code, msg):
        self.id = id
        self.code = code
        self.message = msg

    def to_response(self):
        defined_message = CODE_TO_MESSAGE[self.code]
        msg = f'{defined_message}. {self.message}'

        return {
            'jsonrpc': JSON_RPC_VERSION,
            'error': {
                'code': self.code,
                'message': msg,
            },
            'id': self.id,
        }

    def resulve_async(self, loop):
        pass


class Success:
    def __init__(self, id, result):
        self.id = id
        self.result = result

    def __str__(self):
        return f'Success <{self.id}: {self.result}>'

    def __bool__(self):
        return self.id is not None

    def to_response(self):
        """
        No id request means notification so no response needed
        """
        if self.id is not None:
            return {
                'jsonrpc': JSON_RPC_VERSION,
                'result': self.result,
                'id': self.id,
            }
        return None

    def resolve_async(self, loop):
        """
        FIXME: this is solution.
        Can be Failed after resolved?
        """
        if iscoroutine(self.result):
            self.result = loop.run_until_complete(self.result)
