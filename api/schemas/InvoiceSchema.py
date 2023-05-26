from typing import List
from pydantic import BaseModel

class InvoiceBaseSchema(BaseModel):
    contract_number: str
    customer_number: str
    invoice_type: str
    invoice_date: str
    tva: int = 18
    total_amount_ht: float
    total_amount_ttc: float
    amount_paid: float
    status: str

class Dunning(BaseModel):
    name: str
    date: str
    rank: int
    delay_penalty_rate: float
    total_amount_ht: float
    total_amount_ttc: float
    payment_deadline: int


class PrepaidInfoSchema(InvoiceBaseSchema):
    power_recharged: float
    last_power_recharged: float
    total_power_recharged: float
    status = "paid"
    invoice_type = "prepaid"


class PostpaidInfoSchema(InvoiceBaseSchema):
    index_value: float
    last_index_value: float
    total_power_consumed: float
    remaining_amount: float
    payment_deadline: int
    deadline_measurement_unit: str
    invoicing_frequency: int
    previous_status: str
    status = "not_paid"
    invoice_type = "manual postpaid"
    dunning_max: int
    dunning: List[Dunning]
