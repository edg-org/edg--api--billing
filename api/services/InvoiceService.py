from datetime import datetime
from typing import List, Optional
from api.models.Invoice import Invoice
from fastapi import Depends, HTTPException
from api.repositories.InvoiceRepository import InvoiceRepository

class InvoiceService:
    invoiceRepository: InvoiceRepository

    def __init__(
        self,
        invoiceRepository: InvoiceRepository = Depends()
    ) -> None:
        self.invoiceRepository = invoiceRepository

    def _get_invoice_by_number(self, invoice_type: str, invoice_number: str) -> Optional[Invoice]:
        """
        Get invoice (postpaid or prepaid) by number.

        Args:
            invoice_type: the invoice type (postpaid or prepaid).
            invoice_number: the invoice number.

        Returns:
            Optional Invoice
        """
        return self.invoiceRepository.get_invoice_by_number(
            invoice_type = invoice_type,
            invoice_number = invoice_number,
            is_admin = True # TODO: this parameter depends up user scope (admin or not admin).
        )

    def _delete_invoice(self, invoice_type: str, invoice_number: str) -> None:
        """
        Delete invoice (postpaid or prepaid) by invoice type and number (meaning deactivate the invoice).

        Args:
            invoice_type: the invoice type (postpaid or prepaid).
            invoice_number: the invoice number.

        Returns:
            None
        """
        invoice: Invoice = self._get_invoice_by_number(invoice_type, invoice_number)
        if not invoice:
            ExceptionService.invoice_not_found()

        invoice.is_activated = False
        invoice.updated_at = invoice.deleted_at = datetime.now()
        self.invoiceRepository.delete_invoice(invoice)

    def _get_invoice_by_contract_number(self, invoice_type: str, contract_number: str, offset: int, limit: int) -> List[Invoice]:
        """
        Get invoice by contract number.

        Args:
            contract_number: the contract number.
            offset: the offset.
            limit: the limit.

        Returns:
            List[Invoice]
        """
        return self.invoiceRepository.get_invoice_by_contract_number(
            invoice_type = invoice_type,
            contract_number = contract_number,
            offset = offset,
            limit = limit,
            is_admin = True # TODO: this parameter depends up user scope (admin or not admin).
        )

    def _get_last_invoice_by_contract_number(self, invoice_type: str, contract_number: str) -> Invoice:
        """
        Get last invoice by contract number.

        Args:
            contract_number: the contract number.

        Returns:
           Invoice
        """
        return self.invoiceRepository.get_last_invoice_by_contract_number(
            invoice_type = invoice_type,
            contract_number = contract_number,
            is_admin = True # TODO: this parameter depends up user scope (admin or not admin).
        )