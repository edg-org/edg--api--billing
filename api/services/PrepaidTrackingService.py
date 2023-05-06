from typing import List, Optional
from fastapi import Depends
from api.models.ConsumptionTracking import ConsumptionTracking
from api.repositories.ConsumptionTrackingRepository import ConsumptionTrackingRepository
from api.schemas.pydantic.ConsumptionTrackingSchema import PrepaidCreateSchema, PrepaidInfoSchema
from datetime import datetime
from api.services.ConsumptionTrackingService import ConsumptionTrackingService
from api.services.UtilsService import UtilsService
from fastapi.encoders import jsonable_encoder


class PrepaidTrackingService(ConsumptionTrackingService):
    consumptionTrackingRepository: ConsumptionTrackingRepository

    def __init__(
            self,
            consumptionTrackingRepository: ConsumptionTrackingRepository = Depends()
    ) -> None:
        super().__init__(consumptionTrackingRepository)
        self.consumptionTrackingRepository = consumptionTrackingRepository


    def _build_prepaid_info_schema(self, prepaid_schema: PrepaidCreateSchema) -> PrepaidInfoSchema:
         """
         Build Prepaid Info Schema (PrepaidInfoSchema).

         Args:
             prepaid_schema: the prepaid creation schema (PrepaidCreateSchema).

         Returns:
             PrepaidInfoSchema
         """
         last_tracking = self.get_last_prepaid_tracking_by_contract_number(prepaid_schema.contract_number)
         return PrepaidInfoSchema(
            contract_number = prepaid_schema.contract_number,
            customer_number = "",
            power_recharged = prepaid_schema.power_recharged,
            power_recharged_date = prepaid_schema.power_recharged_date,
            last_power_recharged = 0.00 if last_tracking is None else last_tracking.infos['power_recharged'],
            last_power_recharged_date = "" if last_tracking is None else last_tracking.infos['power_recharged_date'],
            total_power_recharged = prepaid_schema.power_recharged if last_tracking is None else last_tracking.infos['total_power_recharged'] + prepaid_schema.power_recharged
        )


    def create_prepaid_tracking(self, prepaid_schema_list: List[PrepaidCreateSchema], prepaidInvoiceService) -> List[PrepaidCreateSchema]:
        """
         Prepaid tracking creation.

         Args:
             prepaid_schema_list: the list of prepaid schema to create.
             prepaidInvoiceService: the prepaid invoice service.

         Returns:
             List[PrepaidCreateSchema]: the list of created postpaid tracking.
         """
        tracking_list: List[ConsumptionTracking] = []
        created_list: List[PostpaidCreateSchema] = []
        tracking_number_list: list[str] = []

        for prepaid_schema in prepaid_schema_list:
            # TODO: check contract number (prepaid_schema.contract_number) validity with subscriber end-point
            prepaid_info_schema = self._build_prepaid_info_schema(prepaid_schema)
            tracking = ConsumptionTracking(
                tracking_number = UtilsService.generate_uuid(),
                infos = jsonable_encoder(prepaid_info_schema)
            )
            tracking_list.append(tracking)
            created_list.append(prepaid_schema)
            tracking_number_list.append(tracking.tracking_number)

        self.consumptionTrackingRepository.create_tracking(tracking_list) # create tracking prepaid
        prepaidInvoiceService.create_prepaid_invoices(tracking_number_list) # create prepaid invoices
        return created_list # return created list


    def get_prepaid_tracking_by_number(self, tracking_number: str)-> ConsumptionTracking:
        """
        Get prepaid tracking by number.

        Args:
            tracking_number: the tracking number.

        Returns:
            ConsumptionTracking.
        """
        return self._get_tracking_by_number(UtilsService.PREPAID, tracking_number)


    def delete_prepaid_tracking_by_number(self, tracking_number: str)-> None:
        """
        Delete prepaid tracking by number.

        Args:
            tracking_number: the tracking number.

        Returns:
            None.
        """
        self._delete_tracking(UtilsService.PREPAID, tracking_number)


    def get_prepaid_tracking_by_contract_number(self, contract_number: str, offset: int, limit: int)-> List[ConsumptionTracking]:
        """
        Get prepaid tracking by contract number.

        Args:
            contract_number: the contract number.
            offset: the offset
            limit: the limit

        Returns:
            List[ConsumptionTracking]: List of ConsumptionTracking
        """
        return self._get_tracking_by_contract_number(UtilsService.PREPAID, contract_number, offset, limit)


    def get_last_prepaid_tracking_by_contract_number(self, contract_number: str)-> ConsumptionTracking:
        """
        Get last prepaid tracking by contract number.

        Args:
            contract_number: the contract number.

        Returns:
            Optional ConsumptionTracking
        """
        return self._get_last_tracking_by_contract_number(UtilsService.PREPAID, contract_number)


    def get_invoiced_prepaid_tracking_by_number(self, tracking_number: str) -> Optional[ConsumptionTracking]:
        """
        Get invoiced prepaid tracking by number.

        Args:
            tracking_number: the tracking number.

        Returns:
            Optional ConsumptionTracking
        """
        return self._get_tracking_by_type_and_number_and_status(UtilsService.PREPAID, tracking_number, True)
