from .base import UPSBase
import json


class UPSRating(UPSBase):
    """
    Get a rate for a UPS package
    """    
    TESTING_URL = 'https://wwwcie.ups.com/rest/Rate'
    PRODUCTION_URL = 'https://onlinetools.ups.com/rest/Rate'


    def __init__(self, account, password, ship_to, shipper,
            license_number=None, debug=False):
        """
        Store the data for a rate request that is consistent over multiple package
        requests
        """
        
        super().__init__(account, password, ship_to, shipper, license_number,
                debug)

        self.request_data['RateRequest'] = {
                'Request': {
                    'RequestOption': 'Rate',
#                    'TransactionReference': {
#                        'CustomerContext': XXX, #TODO: Customer context? Order number?
#                        }
                    }
                }


    def get_package_rate(self, length, width, height, weight):
        """
        Get a rate from the UPS shipping API for a single package.

        Args:
        - length: Package length (in inches)
        - width: Package width (in inches)
        - height: Package height (in inches)
        - weight: Package weight (in pounds - lb)
        """
        request_data = self.request_data.copy()

        request_data['Service'] = {
                'Code': '03',
                'Description': 'Ground'
                }

        request_data['Package'] = {
                'PackagingType': {
                    'Code': '02',
                    'Description': 'Package'
                    },
                'Dimensions': {
                    'UnitOfMeasurement': {
                        'Code': 'IN',
                        'Description': 'inches'
                        },
                    'Length': length,
                    'Width': width,
                    'Height': height
                    },
                'PackageWeight': {
                    'UnitOfMeasurement': {
                        'Code': 'LBS',
                        'Description': 'Pounds'
                        },
                    'Weight': weight
                    }
                }

        # TODO: Allow this to be sent in
        request_data['ShipmentRatingOptions'] = {
                'NegotiatedRatesIndicator': False
                }

        # TODO: Custom exceptions
        rate_response = self.request(request)

        return rate_response['RatedShipment']['TotalCharges']

