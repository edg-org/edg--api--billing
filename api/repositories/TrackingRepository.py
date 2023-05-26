from typing import List, Optional

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from api.configs.Database import get_db_connection
from api.models.ConsumptionTracking import ConsumptionTracking


class TrackingRepository:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db_connection)
    ) -> None:
        self.db = db


    # create tracking
    def create_tracking(self, tracking_list: List[ConsumptionTracking]) -> List[ConsumptionTracking]:
        self.db.add_all(tracking_list)
        self.db.commit()
        return tracking_list


    # delete tracking : meaning deactivate the tracking consumption
    def delete_tracking(self, consumptionTracking: ConsumptionTracking) -> None:
        self.db.merge(consumptionTracking)
        self.db.commit()


    # update is_invoiced value for only postpaid tracking
    def update_tracking_postpaid(self, consumptionTracking: ConsumptionTracking) -> None:
        self.db.merge(consumptionTracking)
        self.db.commit()


    # get tracking by tracking number
    def get_tracking_by_number(self, tracking_type: str, tracking_number: str, is_admin: bool) -> Optional[ConsumptionTracking]:
         if is_admin:
             query = select(ConsumptionTracking) .filter(
                 ConsumptionTracking.infos['tracking_type'].as_string().ilike('%' + tracking_type + '%'),
                 ConsumptionTracking.tracking_number.ilike(tracking_number)
             )
         else:
             query = select(ConsumptionTracking) .filter(
                 ConsumptionTracking.infos['tracking_type'].as_string().ilike('%' + tracking_type + '%'),
                 ConsumptionTracking.tracking_number.ilike(tracking_number),
                 ConsumptionTracking.is_activated == True
             )

         return self.db.scalars(query).first()


    # get tracking by type and number and status
    def get_tracking_by_type_and_number_and_status(self, tracking_type: str, tracking_number: str, is_invoiced: bool) -> Optional[ConsumptionTracking]:
         query = select(ConsumptionTracking) .filter(
                 ConsumptionTracking.infos['tracking_type'].as_string().ilike('%' + tracking_type + '%'),
                 ConsumptionTracking.tracking_number.ilike(tracking_number),
                 ConsumptionTracking.infos['is_invoiced'] == is_invoiced,
                 ConsumptionTracking.is_activated == True
             )

         return self.db.scalars(query).first()


    # get tracking by contract number
    def get_tracking_by_contract_number(
            self,
            tracking_type: str,
            contract_number: str,
            offset: int,
            limit: int,
            is_admin: bool ) -> List[ConsumptionTracking]:
         if is_admin:
             query = select(ConsumptionTracking) .filter(
                 ConsumptionTracking.infos['tracking_type'].as_string().ilike('%' + tracking_type + '%'),
                 ConsumptionTracking.infos['contract_number'].as_string().ilike(contract_number)
             ).offset(offset).limit(limit)
         else:
             query = select(ConsumptionTracking) .filter(
                 ConsumptionTracking.infos['tracking_type'].as_string().ilike('%' + tracking_type + '%'),
                 ConsumptionTracking.infos['contract_number'].as_string().ilike(contract_number),
                 ConsumptionTracking.is_activated == True
             ).offset(offset).limit(limit)

         return self.db.scalars(query).all()


    # get last tracking by contract number
    def get_last_tracking_by_contract_number(self, tracking_type: str, contract_number: str, is_admin: bool) -> ConsumptionTracking:
         if is_admin:
             query = select(ConsumptionTracking) .filter(
                 ConsumptionTracking.infos['tracking_type'].as_string().ilike('%' + tracking_type + '%'),
                 ConsumptionTracking.infos['contract_number'].as_string().ilike(contract_number)
             ).order_by(desc(ConsumptionTracking.created_at))
         else:
             query = select(ConsumptionTracking) .filter(
                 ConsumptionTracking.infos['tracking_type'].as_string().ilike('%' + tracking_type + '%'),
                 ConsumptionTracking.infos['contract_number'].as_string().ilike(contract_number),
                 ConsumptionTracking.is_activated == True
             ).order_by(desc(ConsumptionTracking.created_at))

         return self.db.scalars(query).first()
