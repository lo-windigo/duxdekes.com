
class UnrecognizedException(Exception):
    pass

class UnknownOperationException(Exception):
    pass

class NetworkException(Exception):
    pass

class JSONSyntaxException(Exception):
    pass

class UnhandledException(Exception):
    pass


def UPSException(code, msg=None):
    """
    A exception factory function: return the proper exception type based on code
    """
    codes = {
            1: UnrecognizedException(msg),
            2: UnknownOperationException(msg),
            3: NetworkException(msg),
            4: JSONSyntaxException(msg),
            }

    if code in codes:
        return codes[code]
    else
        return UnhandledException(msg)

