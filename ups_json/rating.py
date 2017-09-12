from decimal import Decimal as D
from .base import UPSBase
from .exception import UPSException
from .util.dict import get_nested
import json


class UPSRating(UPSBase):
    """
    Get a rate for a UPS package
    """    
    TESTING_URL = 'https://wwwcie.ups.com/rest/Rate'
    #PRODUCTION_URL = 'https://onlinetools.ups.com/rest/Rate'
    PRODUCTION_URL = 'https://atlas.fragdev.net'

 
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
        rated_shipment = self.request_rate(length, width, height, weight,
                ship_to, shipper, ship_from)

        transport = D(get_nested(rated_shipment, 'TransportationCharges',
            'MonetaryValue'))

        # TODO: Add all interesting information to this value
        rates = {
                'transport': transport,
                }
        return D()


    def request_rate(self, length, width, height, weight, ship_to, shipper,
                ship_from=None):
        """
        Submit a rate request to the UPS shipping API, and return the resulting
        dictionary.
        """
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

        # TODO: Allow this to be sent in
        shipment.update({
               'ShipmentRatingOptions': {
                   'NegotiatedRatesIndicator': '',
                   },
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

    #        return json.dumps(rate_request)

        try:
            return rate_response['RateResponse']['RatedShipment']
        except:
            keys = ('Response', 'ResponseStatus', 'Code')
            code = get_nested(rate_response, *keys)
            raise GetUPSException(code)

