from fastapi import Depends
from datetime import datetime
from pydantic import parse_obj_as
from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from api.services.UtilsService import UtilsService
from api.services.TrackingService import TrackingService
from api.models.ConsumptionTracking import ConsumptionTracking
from api.repositories.TrackingRepository import TrackingRepository
from api.schemas.TrackingSchema import PostpaidCreateSchema, PostpaidInfoSchema

class PostpaidTrackingService(TrackingService):
    consumptionTrackingRepository: TrackingRepository

    def __init__(
            self,
            consumptionTrackingRepository: TrackingRepository = Depends()
    ) -> None:
        super().__init__(consumptionTrackingRepository)
        self.consumptionTrackingRepository = consumptionTrackingRepository

    def _build_postpaid_info_schema(self, postpaid_schema: PostpaidCreateSchema) -> PostpaidInfoSchema:
         """
         Build Postpaid Info Schema (PostpaidInfoSchema).

         Args:
             postpaid_schema: the postpaid creation schema (PostpaidCreateSchema).

         Returns:
             PostpaidInfoSchema
         """
         last_tracking = self.get_last_postpaid_tracking_by_contract_number(postpaid_schema.contract_number)
         return PostpaidInfoSchema(
            contract_number = postpaid_schema.contract_number,
            customer_number = "",
            index_value = postpaid_schema.index_value,
            index_date = postpaid_schema.index_date,
            last_index_value = 0.00 if last_tracking is None else last_tracking.infos['index_value'],
            last_index_date = "" if last_tracking is None else last_tracking.infos['index_date'],
            total_power_consumed = postpaid_schema.index_value if last_tracking is None else last_tracking.infos['total_power_consumed'] + postpaid_schema.index_value,
            total_accumulated_period = postpaid_schema.index_value, # TODO: recalculate
            next_tracking_date = ""
        )

    def create_postpaid_tracking(self, postpaid_schema_list: List[PostpaidCreateSchema]) -> List[PostpaidCreateSchema]:
         """
         Postpaid tracking creation.

         Args:
             postpaid_schema_list: the list of postpaid schema to create.

         Returns:
             List[PostpaidCreateSchema]: the list of created postpaid tracking.
         """
         tracking_list: List[ConsumptionTracking] = []
         created_list: List[PostpaidCreateSchema] = []

         for postpaid_schema in postpaid_schema_list:
             # TODO: check contract number (postpaid_schema.contract_number) validity with subscriber end-point
             postpaid_info_schema = self._build_postpaid_info_schema(postpaid_schema)
             tracking = ConsumptionTracking(
                 tracking_number = UtilsService.generate_uuid(),
                 infos = jsonable_encoder(postpaid_info_schema)
             )
             tracking_list.append(tracking)
             created_list.append(postpaid_schema)

         self.consumptionTrackingRepository.create_tracking(tracking_list)
         return  created_list

    def get_postpaid_tracking_by_number(self, tracking_number: str)-> ConsumptionTracking:
        """
        Get postpaid tracking by number.

        Args:
            tracking_number: the tracking number.

        Returns:
            ConsumptionTracking.
        """
        return self._get_tracking_by_number(UtilsService.POSTPAID, tracking_number)

    def delete_postpaid_tracking_by_number(self, tracking_number: str)-> None:
        """
        Delete postpaid tracking by number.

        Args:
            tracking_number: the tracking number.

        Returns:
            None.
        """
        self._delete_tracking(UtilsService.POSTPAID, tracking_number)

    def get_postpaid_tracking_by_contract_number(self, contract_number: str, offset: int, limit: int)-> List[ConsumptionTracking]:
        """
        Get postpaid tracking by contract number.

        Args:
            contract_number: the contract number.
            offset: the offset
            limit: the limit

        Returns:
            List[ConsumptionTracking]: List of ConsumptionTracking
        """
        return self._get_tracking_by_contract_number(UtilsService.POSTPAID, contract_number, offset, limit)

    def get_last_postpaid_tracking_by_contract_number(self, contract_number: str)-> Optional[ConsumptionTracking]:
        """
        Get last postpaid tracking by contract number.

        Args:
            contract_number: the contract number.

        Returns:
            Optional ConsumptionTracking
        """
        return self._get_last_tracking_by_contract_number(UtilsService.POSTPAID, contract_number)

    def get_not_invoiced_postpaid_tracking_by_number(self, tracking_number: str) -> Optional[ConsumptionTracking]:
        """
        Get only not invoiced postpaid tracking by number.

        Args:
            tracking_number: the tracking number.

        Returns:
            Optional ConsumptionTracking
        """
        return self._get_tracking_by_type_and_number_and_status(UtilsService.POSTPAID, tracking_number, False)

    def update_postpaid_tracking(self, tracking_list: List[ConsumptionTracking]) -> None:
        """
        update postpaid tracking.

        Args:
            tracking_list: the contract number.

        Returns:
            Optional ConsumptionTracking
        """
        for tracking in tracking_list:
            infos = parse_obj_as(PostpaidInfoSchema, tracking.infos)
            infos.is_invoiced = True
            tracking.infos = jsonable_encoder(infos)
            tracking.updated_at = datetime.now()
            self.consumptionTrackingRepository.update_tracking_postpaid(tracking)