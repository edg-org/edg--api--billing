from pydantic import BaseModel

class ConsumptionBaseSchema(BaseModel):
    contract_number: str
    customer_number: str
    tracking_type: str
    is_invoiced: bool

class PrepaidInfoSchema(ConsumptionBaseSchema):
    power_recharged: float
    power_recharged_date: str
    last_power_recharged: float
    last_power_recharged_date: str
    total_power_recharged: float
    tracking_type = "prepaid"
    is_invoiced = True

class PostpaidInfoSchema(ConsumptionBaseSchema):
    index_value: float
    index_date: str
    last_index_value: float
    last_index_date: str
    total_power_consumed: float
    total_accumulated_period: float
    next_tracking_date: str
    tracking_type = "manual postpaid"
    is_invoiced = False

class PrepaidCreateSchema(BaseModel):
    contract_number: str
    power_recharged: float
    power_recharged_date: str

class PostpaidCreateSchema(BaseModel):
    contract_number: str
    index_value: float
    index_date: str