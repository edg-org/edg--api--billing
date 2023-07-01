from typing import List
from pydantic import BaseModel

class Slice(BaseModel):
    name: str
    lower_index: float
    upper_index: float
    unit_price: float

class PostpaidPricing(BaseModel):
    domestic: List[Slice]
    private_level1: List[Slice]
    private_level2: List[Slice]
    institution: List[Slice]
    administration: List[Slice]

class PrepaidPricing(BaseModel):
    domestic_level1: List[Slice]
    domestic_level2: List[Slice]
    professional_level1: List[Slice]
    professional_level2: List[Slice]
