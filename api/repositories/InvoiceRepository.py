from typing import List, Optional

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, desc
from api.configs.Database import get_db_connection
from api.models.Invoice import Invoice


class InvoiceRepository:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db_connection)
    ) -> None:
        self.db = db


    # create invoices
    def create_invoices(self, invoices: List[Invoice]) -> List[Invoice]:
        self.db.add_all(invoices)
        self.db.commit()
        return invoices


    # update invoice
    def update_invoice(self, invoice: Invoice) -> None:
        self.db.merge(invoice)
        self.db.commit()


    # delete invoice : meaning deactivate the invoice
    def delete_invoice(self, invoice: Invoice) -> None:
        self.db.merge(invoice)
        self.db.commit()


    # get invoice by number
    def get_invoice_by_number(self, invoice_type: str, invoice_number: str, is_admin: bool) -> Optional[Invoice]:
         if is_admin:
             query = select(Invoice).filter(
                 Invoice.infos['invoice_type'].as_string().ilike('%' + invoice_type + '%'),
                 Invoice.invoice_number.ilike(invoice_number)
             )
         else:
             query = select(Invoice).filter(
                 Invoice.infos['invoice_type'].as_string().ilike('%' + invoice_type + '%'),
                 Invoice.invoice_number.ilike(invoice_number),
                 Invoice.is_activated == True
             )

         return self.db.scalars(query).first()


    # get invoice by contract number
    def get_invoice_by_contract_number(
            self,
            invoice_type: str,
            contract_number: str,
            offset: int,
            limit: int,
            is_admin: bool ) -> List[Invoice]:
         if is_admin:
             query = select(Invoice).filter(
                 Invoice.infos['invoice_type'].as_string().ilike('%' + invoice_type + '%'),
                 Invoice.infos['contract_number'].as_string().ilike(contract_number)
             ).offset(offset).limit(limit)
         else:
             query = select(Invoice).filter(
                 Invoice.infos['invoice_type'].as_string().ilike('%' + invoice_type + '%'),
                 Invoice.infos['contract_number'].as_string().ilike(contract_number),
                 Invoice.is_activated == True
             ).offset(offset).limit(limit)

         return self.db.scalars(query).all()


    # get last invoice by contract number
    def get_last_invoice_by_contract_number(self, invoice_type: str, contract_number: str, is_admin: bool) -> Invoice:
         if is_admin:
             query = select(Invoice) .filter(
                 Invoice.infos['invoice_type'].as_string().ilike('%' + invoice_type + '%'),
                 Invoice.infos['contract_number'].as_string().ilike(contract_number)
             ).order_by(desc(Invoice.created_at))
         else:
             query = select(Invoice) .filter(
                 Invoice.infos['invoice_type'].as_string().ilike('%' + invoice_type + '%'),
                 Invoice.infos['contract_number'].as_string().ilike(contract_number),
                 Invoice.is_activated == True
             ).order_by(desc(Invoice.created_at))

         return self.db.scalars(query).first()
