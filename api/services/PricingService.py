from api.schemas.pydantic.PricingSchema import Slice, PostpaidPricing, PrepaidPricing

class PricingService:
    def __init__(self):
            self.postpaid_pricing = PostpaidPricing(
                domestic = [
                        Slice(name = "Slice 1", lower_index = 1.00, upper_index = 40.00, unit_price = 90.00),
                        Slice(name = "Slice 2", lower_index = 41.00, upper_index = 330.00, unit_price = 293.00),
                        Slice(name = "Slice 3", lower_index = 331.00, upper_index = 1000000000.00, unit_price = 336.00)
                ],
               private_level1 = [],
               private_level2 = [],
               institution = [],
               administration = []
            ) # TODO: these data must be to retrieve from referential end-point or from this microservice local table

            self.prepaid_pricing = PrepaidPricing(
                domestic_level1 = [
                        Slice(name = "Slice 1", lower_index = 1.00, upper_index = 40.00, unit_price = 255.00),
                        Slice(name = "Slice 2", lower_index = 41.00, upper_index = 1000000000.00, unit_price = 347.00)
                ],
               domestic_level2 = [Slice(name = "Slice unique", lower_index = 1.00, upper_index = 1000000000.00, unit_price = 359.00)],
               institution_level1 = [],
               institution_level2 = []
            ) # TODO: these data must be to retrieve from referential end-point or from this microservice local table


    def get_postpaid_unit_price(self, index_value) -> float:
        slice = [slice for slice in self.postpaid_pricing.domestic if slice.lower_index <= index_value <= slice.upper_index][-1]
        return slice.unit_price


    def get_prepaid_unit_price(self, power_subscriber) -> float:
        slice = [slice for slice in self.prepaid_pricing.domestic_level1 if slice.lower_index <= power_subscriber <= slice.upper_index][-1]
        return slice.unit_price

