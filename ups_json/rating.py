import logging
from decimal import Decimal as D
from . import exception
from .base import UPSBase
from .util.dict import get_nested
import json
import statestyle


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# DEBUG LOGGING
import sys
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class UPSRating(UPSBase):
    """
    Get a rate for a UPS package
    """    
    TESTING_URL = 'https://wwwcie.ups.com/rest/Rate'
    PRODUCTION_URL = 'https://onlinetools.ups.com/rest/Rate'
    #PRODUCTION_URL = 'https://atlas.fragdev.net'

 
    def __init__(self, account, password, license_number, testing=False, negotiated=False):
        """
        Override the constructor to also accept a flag for negotiated rates
        """
        super().__init__(account, password, license_number, testing)
        self.negotiated = negotiated


    def get_rate(self, length, width, height, weight, ship_to, shipper, ship_from=None):
        """
        Get a rate from the UPS shipping API for a single package.

        Args:
        - length: Package length (in inches)
        - width: Package width (in inches)
        - height: Package height (in inches)
        - weight: Package weight (in pounds - lb)
        - ship_to: The package destination
        - shipper: The person shipping the package
        - ship_from: Where the package will be shipping from (optional)

        Returns:
        A single Decimal (D) with the total package rate
        """
        rated_shipment = self.request_rate(length, width, height, weight,
                ship_to, shipper, ship_from)

        return D(get_nested(rated_shipment, 'TotalCharges', 'MonetaryValue'))


    def get_rate_details(self, length, width, height, weight, ship_to, shipper, ship_from=None):
        """
        Get a dict containing detailed rate information from the UPS shipping
        API for a single package.

        Args:
        - length: Package length (in inches)
        - width: Package width (in inches)
        - height: Package height (in inches)
        - weight: Package weight (in pounds - lb)
        - ship_to: The package destination
        - shipper: The person shipping the package
        - ship_from: Where the package will be shipping from (optional)

        Returns:
        {
            
        }
        """
        raise NotImplemented

        rated_shipment = self.request_rate(length, width, height, weight,
                ship_to, shipper, ship_from)

        transport = D(get_nested(rated_shipment, 'TransportationCharges',
            'MonetaryValue'))

        # TODO: Add all interesting information to this value
        rates = {
                'transport': transport,
                }
        return D()


    def prepare_address(self, address):
        """
        Take an address object and apply data adjustments to allow it to conform
        to the requirements of the UPS API
        """

        # Only use state postal abbreviations
        try:
            if address.get('country_code', '') == 'US':
                state = statestyle.get(address['state_province'])
                address['state_province'] = state.postal
        except KeyError as e:
            # Ignore exceptions if these fields aren't set
            pass
        #except ValueError as e:
            # Ignore if the library cannot find a state
            #pass

        return address


    def request_rate(self, length, width, height, weight, ship_to, shipper,
                ship_from=None):
        """
        Submit a rate request to the UPS shipping API, and return the resulting
        dictionary.
        """

        shipper = self.prepare_address(shipper)
        ship_to = self.prepare_address(ship_to)

        # Process ship to, ship from, and shipper addresses as needed
        shipment = {
                'ShipTo': {
                    'Name': ship_to.get('name', ''),
                    'Address': {
                        'AddressLine': ship_to.get('address_lines', []),
                        'City': ship_to.get('city', ''),
                        'StateProvinceCode': ship_to.get('state_province', ''),
                        'PostalCode': ship_to.get('postal_code', ''),
                        'CountryCode': ship_to.get('country_code', ''),
                        },
                    },
                'Shipper': {
                    'Name': shipper.get('name', ''),
                    #'ShipperNumber': account_number,
                    'Address': {
                        'AddressLine': shipper.get('address_lines', []),
                        'City': shipper.get('city', ''),
                        'StateProvinceCode': shipper.get('state_province', ''),
                        'PostalCode': shipper.get('postal_code', ''),
                        'CountryCode': shipper.get('country_code', ''),
                        },
                    },
                'Package': {
                    'PackagingType': {
                        'Code': '02',
                        'Description': 'Package',
                        },
                    'Dimensions': {
                        'UnitOfMeasurement': {
                            'Code': 'IN',
                            'Description': 'inches',
                            },
                        'Length': str(length),
                        'Width': str(width),
                        'Height': str(height),
                        },
                    'PackageWeight': {
                        'UnitOfMeasurement': {
                            'Code': 'LBS',
                            'Description': 'Pounds',
                            },
                        'Weight': str(weight),
                        },
                    },
                }

        # If an optional ship_from is specified, add it
        if ship_from:
            ship_from = self.prepare_address(ship_from)
            shipment.update({
                'ShipFrom': {
                    'Name': ship_from.get('name', ''),
                    'Address': {
                        'AddressLine': ship_from.get('address_lines', ''),
                        'City': ship_from.get('city', ''),
                        'StateProvinceCode': ship_from.get('state_province', ''),
                        'PostalCode': ship_from.get('postal_code', ''),
                        'CountryCode': ship_from.get('country_code', ''),
                        },
                    }
                })

        #TODO: Other services are available
        shipment.update({
                'Service': {
                    'Code': '03',
                    'Description': 'Ground'
                    }
                })

        request = {
                'RequestOption': 'Rate',
    #                    'TransactionReference': {
    #                        'CustomerContext': XXX, #TODO: Customer context? Order number?
    #                        }
                }

        pickup_type = {
                'Code': '01',
                }

        rate_request = {
                'RateRequest': {
                    'Shipment': shipment,
                    'Request': request,
                    'PickupType': pickup_type,
                    },
                'UPSSecurity': self.security_token,
                }

        if self.negotiated:
            rate_request['RateRequest'].update({
                   'ShipmentRatingOptions': {
                       'NegotiatedRatesIndicator': True, 
                       },
                   })

        # Make the request to the UPS API
        rate_response = self.request(rate_request)

        logger.info('UPS API response for box (%sx%sx%s) weighing %s: %s',
                length, width, height, weight, rate_response)

        try:
            return rate_response['RateResponse']['RatedShipment']
        except:
            if 'Fault' in rate_response:
                base_keys = 'Fault', 'detail', 'Errors', 'ErrorDetail', \
                    'PrimaryErrorCode'

                code_keys = base_keys + ('Code',)
                code = get_nested(rate_response, *code_keys)

                error_keys = base_keys + ('Description',)
                error_description = get_nested(rate_response, *error_keys)

                e = exception.GetException(code, error_description)

            if 'Error' in rate_response:
                code = get_nested(rate_response, 'Error', 'Code')
                error = get_nested(rate_response, 'Error', 'Description')

                e = exception.GetSimpleException(code, error)

            else:
                error = 'Unknown error: {}'.format(json.dumps(rate_response))

                e = exception.UnhandledException(error)

            # ...from None stops the nested exception reporting
            raise e from None

