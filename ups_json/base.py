
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

    def __init__(self, account, password, ship_to, shipper, ship_from=None,
            license_number=None, testing=False):
        """
        Save user credentials, values to the request data

        Args:
        - TODO
        """
        self.request_data['UPSSecurity'] = {
                'Username': account,
                'Password': password,
                }

#        self.request_data['ServiceAccessToken'] = {
#                'AccessLicenseNumber': license_number,
#                }

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
                'Shipper': {
                    'Name': shipper.name,
                    #'ShipperNumber': account_number,
                    'Address': {
                        'AddressLine': shipper.address_lines,
                        'City': shipper.city,
                        'StateProvinceCode': shipper.state_province,
                        'PostalCode': shipper.postal_code,
                        'CountryCode': shipper.country_code
                    },
                }
            }

        # If an optional ship_from is specified, add it
        if ship_from:
            self.request_data['Shipment'].extend({
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
                })

        self.testing = testing

    def request(self, request_data=None):
        """
        Take in the required information, and encode it in the JSON format that
        is required by the UPS API
        """
        if not request_data:
            request_data = self.request_data

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

