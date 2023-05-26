from typing import List, Optional
from fastapi import Depends
from api.models.ConsumptionTracking import ConsumptionTracking
from api.repositories.TrackingRepository import TrackingRepository
from datetime import datetime
from api.services.ExceptionService import ExceptionService


class TrackingService:
    consumptionTrackingRepository: TrackingRepository

    def __init__(
        self,
        consumptionTrackingRepository: TrackingRepository = Depends()
    ) -> None:
        self.consumptionTrackingRepository = consumptionTrackingRepository


    def _get_tracking_by_number(self, tracking_type: str, tracking_number: str) -> Optional[ConsumptionTracking]:
        """
        Get a tracking (postpaid or prepaid) by a tracking number.

        Args:
            tracking_type: the tracking type (postpaid or prepaid).
            tracking_number: the tracking number.

        Returns:
            Optional ConsumptionTracking
        """
        return self.consumptionTrackingRepository.get_tracking_by_number(
            tracking_type = tracking_type,
            tracking_number = tracking_number,
            is_admin = True # TODO: this parameter depends up user scope (admin or not admin).
        )


    def _get_tracking_by_type_and_number_and_status(self, tracking_type: str, tracking_number: str, is_invoiced: bool) -> Optional[ConsumptionTracking]:
        """
        Get a tracking (postpaid or prepaid) by tracking type and number and status (is invoiced or not).

        Args:
            tracking_type: the tracking type (postpaid or prepaid).
            tracking_number: the tracking number.
            is_invoiced: the tracking status (True or False)

        Returns:
            Optional ConsumptionTracking
        """
        return self.consumptionTrackingRepository.get_tracking_by_type_and_number_and_status(
            tracking_type = tracking_type,
            tracking_number = tracking_number,
            is_invoiced = is_invoiced
        )


    def _delete_tracking(self, tracking_type: str, tracking_number: str) -> None:
        """
        Delete tracking (postpaid or prepaid) by tracking type and number (meaning deactivate the tracking).

        Args:
            tracking_type: the tracking type (postpaid or prepaid).
            tracking_number: the tracking number.

        Returns:
            None
        """
        tracking: ConsumptionTracking = self._get_tracking_by_number(tracking_type, tracking_number)
        if not tracking:
            ExceptionService.tracking_not_found()

        tracking.is_activated = False
        tracking.updated_at = tracking.deleted_at = datetime.now()
        self.consumptionTrackingRepository.delete_tracking(tracking)


    def _get_tracking_by_contract_number(self, tracking_type: str, contract_number: str, offset: int, limit: int) -> List[ConsumptionTracking]:
        """
        Get tracking (postpaid or prepaid) by tracking type and contract number.

        Args:
            tracking_type: the tracking type (postpaid or prepaid).
            contract_number: the contract number.
            offset: the offset
            limit: the limit

        Returns:
            List[ConsumptionTracking]: List of ConsumptionTracking
        """
        return self.consumptionTrackingRepository.get_tracking_by_contract_number(
            tracking_type = tracking_type,
            contract_number = contract_number,
            offset = offset,
            limit = limit,
            is_admin = True # TODO: this parameter depends up user scope (admin or not admin).
        )


    def _get_last_tracking_by_contract_number(self, tracking_type: str, contract_number: str) -> ConsumptionTracking:
        """
        Get last tracking (postpaid or prepaid) by tracking type and contract number.

        Args:
            tracking_type: the tracking type (postpaid or prepaid).
            contract_number: the contract number.

        Returns:
            ConsumptionTracking
        """
        return self.consumptionTrackingRepository.get_last_tracking_by_contract_number(
            tracking_type = tracking_type,
            contract_number = contract_number,
            is_admin = True # TODO: this parameter depends up user scope (admin or not admin).
        )
