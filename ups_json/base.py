
import json
from urllib import request


class UPSBase():
    """
    A base for requests to the UPS JSON API
    """
    debug = False
    request_data = {}

    def __init__(self, account, password, license_number=None, testing=False):
        """
        Save user credentials, values to the request data
        """
        self.request_data['UPSSecurity'] = {
                'Username': account,
                'Password': password,
                }

        self.request_data['ServiceAccessToken'] = {
                'AccessLicenseNumber': license_number,
                }

        self.testing = testing

    def request(self):
        """
        Take in the required information, and encode it in the JSON format that
        is required by the UPS API
        """
        json_data = json.dumps(self.request_data)
        url = self.get_url()

        api_request = request.Request(url,
                headers = {
                'Access-Control-Allow-Headers':
                    'Origin, X-Requested-With, Content-Type, Accept',
                'Access-Control-Allow-Methods': 'POST',
                'Access-Control-Allow-Origin': '*',
                'Content-type': 'application/json',
                },
                data = json_data,
                method = 'POST')
        api_response = request.urlopen(api_request)

        return json.loads(api_response.read())

    def get_url(self):
        """
        Get the URL to send the request to
        """
        if self.testing:
            return self.TESTING_URL

        return self.PRODUCTION_URL

