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
