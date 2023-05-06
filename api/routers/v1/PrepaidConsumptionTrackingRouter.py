from typing import List

from fastapi import APIRouter, Depends, status

from api.schemas.pydantic.ConsumptionTrackingSchema import PrepaidCreateSchema, PrepaidInfoSchema
from api.services.PrepaidTrackingService import PrepaidTrackingService
from api.services.PrepaidInvoiceService import PrepaidInvoiceService

PrepaidConsumptionTrackingRouter = APIRouter(prefix="/tracking/prepaid", tags=["prepaid consumption tracking"])

@PrepaidConsumptionTrackingRouter.post(
    "/",
    status_code = status.HTTP_201_CREATED,
    summary = "Create prepaid tracking",
    description = "Create prepaid tracking on bulk depending on the list of contract number"
)
def create_prepaid_tracking(
    prepaid_list: List[PrepaidCreateSchema],
    prepaidTrackingService: PrepaidTrackingService = Depends(),
    prepaidInvoiceService: PrepaidInvoiceService = Depends()
):
    return prepaidTrackingService.create_prepaid_tracking(prepaid_list, prepaidInvoiceService)


@PrepaidConsumptionTrackingRouter.get(
    "/number",
    summary = "Get prepaid tracking by number",
    description = "Get prepaid tracking with the tracking number"
)
def get_prepaid_tracking_by_number(
    tracking_number: str,
    prepaidTrackingService: PrepaidTrackingService = Depends()
):
    return prepaidTrackingService.get_prepaid_tracking_by_number(tracking_number)


@PrepaidConsumptionTrackingRouter.get(
    "/contract_number",
    summary = "Get prepaid tracking by contract number",
    description = "Get prepaid tracking with the contract number"
)
def get_prepaid_by_contract_number(
    contract_number: str,
    offset: int = 0,
    limit: int = 10,
    prepaidTrackingService: PrepaidTrackingService = Depends()
):
    return prepaidTrackingService.get_prepaid_tracking_by_contract_number(contract_number, offset, limit)


@PrepaidConsumptionTrackingRouter.get(
    "/contract_number/last",
    summary = "Get last prepaid tracking by contract number",
    description = "Get last prepaid tracking with the contract number"
)
def get_last_prepaid_by_contract_number(
    contract_number: str,
    prepaidTrackingService: PrepaidTrackingService = Depends()
):
    return prepaidTrackingService.get_last_prepaid_tracking_by_contract_number(contract_number)


@PrepaidConsumptionTrackingRouter.delete(
    "/number",
    summary = "Delete prepaid tracking by number",
    description = "Delete prepaid tracking with the tracking number"
)
def delete_postpaid_tracking_by_number(
    tracking_number: str,
    prepaidTrackingService: PrepaidTrackingService = Depends()
):
    prepaidTrackingService.delete_prepaid_tracking_by_number(tracking_number)
