from typing import Dict, List
from sqlalchemy import String, JSON
from datetime import datetime, date
from api.configs.BaseModel import EntityMeta
from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship, 
    backref
)

class ConsumptionTracking(EntityMeta):
    __tablename__ = "consumption_tracking"

    id: Mapped[int] = mapped_column(primary_key = True)
    tracking_number: Mapped[str] = mapped_column(String(50), unique = True)
    tracking_date: Mapped[date] = mapped_column(nullable = False, index=True)
    is_activated: Mapped[bool] = mapped_column(default = True)
    infos: Mapped[Dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(default = datetime.now())
    updated_at: Mapped[datetime] = mapped_column(nullable = True)
    deleted_at: Mapped[datetime] = mapped_column(nullable = True)
    invoices: Mapped[List["Invoice"]] = relationship(backref = "tracking")

    #__table_args__ = {
    #    'info': {
    #        'mysql_partition': """
    #             PARTITION BY HASH(tracking_date)
    #         """
    #    }
    #}


