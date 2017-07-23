from .base import UPSBase
import json


class UPSRating(UPSBase):
    """
    Get a rate for a UPS package
    """    
    TESTING_URL = 'https://wwwcie.ups.com/rest/Rate'
    #PRODUCTION_URL = 'https://onlinetools.ups.com/rest/Rate'
    PRODUCTION_URL = 'https://atlas.fragdev.net'


    def get_package_rate(self, length, width, height, weight, ship_to, shipper,
            ship_from=None):
        """
        Get a rate from the UPS shipping API for a single package.

        Args:
        - length: Package length (in inches)
        - width: Package width (in inches)
        - height: Package height (in inches)
        - weight: Package weight (in pounds - lb)
        - ship_to: The package destination
        - ship_from: Where the package will be shipping from (optional)
        """
        shipment = {
                'ShipTo': {
                    'Name': ship_to.name,
                    'Address': {
                        'AddressLine': ship_to.address_lines,
                        'City': ship_to.city,
                        'StateProvinceCode': ship_to.state_province,
                        'PostalCode': ship_to.postal_code,
                        'CountryCode': ship_to.country_code,
                        },
                    },
                'Shipper': {
                    'Name': shipper.name,
                    #'ShipperNumber': account_number,
                    'Address': {
                        'AddressLine': shipper.address_lines,
                        'City': shipper.city,
                        'StateProvinceCode': shipper.state_province,
                        'PostalCode': shipper.postal_code,
                        'CountryCode': shipper.country_code,
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

        # TODO: Custom exceptions
        rate_response = self.request(rate_request)

        if 'Response' in rate_response and 
            'ResponseStatus' in rate_response['Response'] and
            'Code' in rate_response['Response']['ResponseStatus'] and
            :
            raise Exception()

        return rate_response
        #return rate_response['RatedShipment']['TotalCharges']

