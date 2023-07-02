from typing import List
from fastapi import APIRouter, Depends, status
from api.configs.Environment import get_env_var
from api.services.PostpaidTrackingService import PostpaidTrackingService
from api.schemas.TrackingSchema import PostpaidCreateSchema, PostpaidCreateSchema

env = get_env_var()
router_path = env.api_routers_prefix + env.api_version

postpaidTrackingRouter = APIRouter(
    prefix=router_path + "/tracking/postpaid",
    tags=["Postpaid Consumption Tracking"],
)

@postpaidTrackingRouter.post(
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


@postpaidTrackingRouter.get(
    "/{number}",
    summary = "Get postpaid tracking by number",
    description = "Get postpaid tracking with the tracking number"
)
def get_postpaid_tracking_by_number(
    number: str,
    postpaidTrackingService: PostpaidTrackingService = Depends()
):
    return postpaidTrackingService.get_postpaid_tracking_by_number(number)


@postpaidTrackingRouter.get(
    "/{contract_number}",
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


@postpaidTrackingRouter.get(
    "/{contract_number}/last",
    summary = "Get last postpaid tracking by contract number",
    description = "Get last postpaid tracking with the contract number"
)
def get_last_postpaid_tracking_by_contract_number(
    contract_number: str,
    postpaidTrackingService: PostpaidTrackingService = Depends()
):
    return postpaidTrackingService.get_last_postpaid_tracking_by_contract_number(contract_number)


@postpaidTrackingRouter.delete(
    "/{number}",
    summary = "Delete postpaid tracking by number",
    description = "Delete postpaid tracking with the tracking number"
)
def delete_postpaid_tracking_by_number(
    number: str,
    postpaidTrackingService: PostpaidTrackingService = Depends()
):
    postpaidTrackingService.delete_postpaid_tracking_by_number(number)
