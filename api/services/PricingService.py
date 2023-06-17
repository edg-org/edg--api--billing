from api.schemas.PricingSchema import Slice, PostpaidPricing, PrepaidPricing
from pydantic import parse_obj_as
from api.services.UtilsService import UtilsService

class PricingService:
    def __init__(self):
            self.postpaid_pricing = parse_obj_as(PostpaidPricing, UtilsService.get_json_data("PostpaidPricing.json"))
            self.prepaid_pricing = parse_obj_as(PrepaidPricing, UtilsService.get_json_data("PrepaidPricing.json"))


    def get_postpaid_unit_price(self, index_value) -> float:
        slice = [slice for slice in self.postpaid_pricing.domestic if slice.lower_index <= index_value <= slice.upper_index][-1]
        return slice.unit_price

    def get_prepaid_unit_price(self, power_subscriber) -> float:
        slice = [slice for slice in self.prepaid_pricing.domestic_level1 if slice.lower_index <= power_subscriber <= slice.upper_index][-1]
        return slice.unit_price
    
