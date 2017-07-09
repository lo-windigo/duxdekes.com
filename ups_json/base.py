
import json


class UPSBase():
    """
    A base for requests to the UPS JSON API
    """
    def __init__(self, account, key, debug=False):
        """
        Save default credentials, values
        """
        self.account = account
        self.api_key = key
        self.debug = debug

