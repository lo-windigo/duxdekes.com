
import json
from urllib import request

class UPSAddress():
    """
    A class built for containing a whole address, and all of its variable parts
    """
    name = None
    address_lines = []
    city = None
    state_province = None
    postal_code = None
    country_code = None


class UPSBase():
    """
    A base for requests to the UPS JSON API
    """
    debug = False
    request_data = {}

    def __init__(self, account, password, ship_to, ship_from,
            license_number=None, testing=False):
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

        self.request_data['Shipment'] = {
                'ShipTo': {
                    'Name': ship_to.name,
                    'Address': {
                        'AddressLine': ship_to.address_lines,
                        'City': ship_to.city,
                        'StateProvinceCode': ship_to.state_province,
                        'PostalCode': ship_to.postal_code,
                        'CountryCode': ship_to.country_code
                        }
                    },
                'ShipFrom': {
                    'Name': ship_from.name,
                    'Address': {
                        'AddressLine': ship_from.address_lines,
                        'City': ship_from.city,
                        'StateProvinceCode': ship_from.state_province,
                        'PostalCode': ship_from.postal_code,
                        'CountryCode': ship_from.country_code
                    },
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

