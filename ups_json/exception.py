
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


def GetUPSException(code, msg=None):
    """
    A exception factory function: return the proper exception type based on code
    """
    codes = {
            1: UnrecognizedException,
            2: UnknownOperationException,
            3: NetworkException,
            4: JSONSyntaxException,
            }

    if code in codes:
        return codes[code](msg)
    else
        return UnhandledException(msg)

