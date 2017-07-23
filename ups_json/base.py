
import json
from urllib import request

class UPSAddress():
    """
    A class built for containing a whole address, and all of its variable parts
    """
    name = None
    address_lines = None
    city = None
    state_province = None
    postal_code = None
    country_code = None

    def __init__(self):
        self.address_lines = []


class UPSBase():
    """
    A base for requests to the UPS JSON API
    """
    debug = False
    security_token = None


    def __init__(self, account, password, license_number, testing=False):
        """
        Save user credentials, values for use in later requests

        Args:
        - account: UPS account username
        - password: UPS password
        - license_number: Your access license number
        - testing: Whether or not the testing API should be used. Default: False
        """
        self.security_token = {
                'UsernameToken': {
                    'Username': account,
                    'Password': password,
                    },
                'ServiceAccessToken': {
                    'AccessLicenseNumber': license_number,
                    }
                }

        self.testing = testing


    def request(self, request_data):
        """
        Take in the required information, and encode it in the JSON format that
        is required by the UPS API
        """
        json_data = json.dumps(request_data).encode('utf-8')
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

        return json.loads(api_response.read().decode('utf-8'))


    def get_url(self):
        """
        Get the URL to send the request to
        """
        try:
            if self.testing:
                return self.TESTING_URL

            return self.PRODUCTION_URL

        except:
            msg = '''
            No API url specified (TESTING_URL or PRODUCTION_URL - must be
            specified by the implementing class!)
            '''
            raise NotImplementedException(msg)

