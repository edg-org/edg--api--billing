from sqlalchemy import String, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from api.models.BaseModel import EntityMeta
from datetime import datetime
from typing import Dict

class Invoice(EntityMeta):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key = True)
    invoice_number: Mapped[str] = mapped_column(String(50), unique = True)
    tracking_id: Mapped[int] = mapped_column(ForeignKey("consumption_tracking.id"))
    is_activated: Mapped[bool] = mapped_column(default = True)
    infos: Mapped[Dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(default = datetime.now())
    updated_at: Mapped[datetime] = mapped_column(nullable = True)
    deleted_at: Mapped[datetime] = mapped_column(nullable = True)
