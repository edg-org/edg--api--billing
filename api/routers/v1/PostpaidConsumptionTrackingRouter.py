from typing import List

from fastapi import APIRouter, Depends, status

from api.schemas.pydantic.ConsumptionTrackingSchema import PostpaidCreateSchema, PostpaidCreateSchema
from api.services.PostpaidTrackingService import PostpaidTrackingService

PostpaidConsumptionTrackingRouter = APIRouter(prefix="/tracking/postpaid", tags=["postpaid consumption tracking"])

@PostpaidConsumptionTrackingRouter.post(
    "/",
    status_code = status.HTTP_201_CREATED,
    summary = "Create postpaid tracking",
    description = "Create postpaid tracking on bulk depending on the list of contract number"
)
def create_postpaid_tracking(
    postpaid_list: List[PostpaidCreateSchema],
    postpaidTrackingService: PostpaidTrackingService = Depends(),
):
    return postpaidTrackingService.create_postpaid_tracking(postpaid_list)


@PostpaidConsumptionTrackingRouter.get(
    "/number",
    summary = "Get postpaid tracking by number",
    description = "Get postpaid tracking with the tracking number"
)
def get_postpaid_tracking_by_number(
    tracking_number: str,
    postpaidTrackingService: PostpaidTrackingService = Depends()
):
    return postpaidTrackingService.get_postpaid_tracking_by_number(tracking_number)


@PostpaidConsumptionTrackingRouter.get(
    "/contract_number",
    summary = "Get postpaid tracking by contract number",
    description = "Get postpaid tracking with the contract number"
)
def get_postpaid_tracking_by_contract_number(
    contract_number: str,
    offset: int = 0,
    limit: int = 10,
    postpaidTrackingService: PostpaidTrackingService = Depends()
):
    return postpaidTrackingService.get_postpaid_tracking_by_contract_number(contract_number, offset, limit)


@PostpaidConsumptionTrackingRouter.get(
    "/contract_number/last",
    summary = "Get last postpaid tracking by contract number",
    description = "Get last postpaid tracking with the contract number"
)
def get_last_postpaid_tracking_by_contract_number(
    contract_number: str,
    postpaidTrackingService: PostpaidTrackingService = Depends()
):
    return postpaidTrackingService.get_last_postpaid_tracking_by_contract_number(contract_number)


@PostpaidConsumptionTrackingRouter.delete(
    "/number",
    summary = "Delete postpaid tracking by number",
    description = "Delete postpaid tracking with the tracking number"
)
def delete_postpaid_tracking_by_number(
    tracking_number: str,
    postpaidTrackingService: PostpaidTrackingService = Depends()
):
    postpaidTrackingService.delete_postpaid_tracking_by_number(tracking_number)
