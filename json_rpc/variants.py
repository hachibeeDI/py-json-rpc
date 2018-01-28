from asyncio import iscoroutine, gather, ensure_future, Future
from enum import Enum
from operator import methodcaller
from itertools import chain


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
        return self


class Success:
    def __init__(self, id, result):
        self.id = id
        self.result = result
        if iscoroutine(self.result):
            print('succeeeeesssss')
            print(self.result)
            self.result = ensure_future(self.result)
            print(self.result)

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

    def is_async(self):
        return isinstance(self.result, Future)

    def resolve_async(self, loop):
        """
        FIXME: this is solution.
        Can be Failed after resolved?
        """
        if self.is_async():
            try:
                self.result = loop.run_until_complete(self.result)
            except Exception as e:
                return Fail(id, ErrorCode.UNEXPECTED_ERROR, str(e))
        return self


class AsyncResultsResolver:
    def __init__(self, results, loop):
        self.results = results
        self.loop = loop
        self.failed = [r for r in results if isinstance(r, Fail)]
        self.successed = [r for r in results if isinstance(r, Success)]

    def to_response(self):
        successed = []
        async_results = []
        for s in self.successed:
            if s.is_async():
                async_results.append(s)
            else:
                successed.append(s)

        resolved_async_result = map(
            lambda i_r: Success(i_r[0], i_r[1]),
            zip(
                (r.id for r in async_results),
                self.loop.run_until_complete(gather(*[r.result for r in async_results])),
            )
        )
        return list(filter(None, map(
            methodcaller('to_response'),
            chain(self.failed, successed, resolved_async_result),
        )))
