
class CredentialsException(Exception):
    pass

class GeneralException(Exception):
    pass

class JSONSyntaxException(Exception):
    pass

class NetworkException(Exception):
    pass

class UnhandledException(Exception):
    pass

class UnknownOperationException(Exception):
    pass

class UnrecognizedException(Exception):
    pass


def GetException(code, msg=None):
    """
    A exception factory function: return the proper exception type based on code
    """
    codes = {
            '10': JSONSyntaxException,
            '20': GeneralException,
            '25': CredentialsException,
            }

    exception_class = codes.get(code[:2], UnhandledException)
    return exception_class(msg)


def GetSimpleException(code, msg=None):
    """
    A exception factory function: return the proper exception type based on code
    """
    codes = {
            1: UnrecognizedException,
            2: UnknownOperationException,
            3: NetworkException,
            4: JSONSyntaxException,
            }

    exception_class = codes.get(code, UnhandledException)
    return exception_class(msg)

