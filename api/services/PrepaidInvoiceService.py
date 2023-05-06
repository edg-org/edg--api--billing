from typing import List, Optional
from fastapi import Depends
from api.models.Invoice import Invoice
from api.models.ConsumptionTracking import ConsumptionTracking
from api.repositories.InvoiceRepository import InvoiceRepository
from datetime import datetime
from api.services.InvoiceService import InvoiceService
from api.services.ExceptionService import ExceptionService
from api.services.PrepaidTrackingService import PrepaidTrackingService
from api.schemas.pydantic.InvoiceSchema import PrepaidInfoSchema
from api.services.UtilsService import UtilsService
from fastapi.encoders import jsonable_encoder
from api.services.PricingService import PricingService


class PrepaidInvoiceService(InvoiceService):
    invoiceRepository: InvoiceRepository
    prepaidTrackingService: PrepaidTrackingService
    pricingService: PricingService

    def __init__(
            self,
            invoiceRepository: InvoiceRepository = Depends(),
            prepaidTrackingService: PrepaidTrackingService = Depends(),
            pricingService: PricingService = Depends()
    ) -> None:
        super().__init__(invoiceRepository)
        self.invoiceRepository = invoiceRepository
        self.prepaidTrackingService = prepaidTrackingService
        self.pricingService = pricingService


    def build_prepaid_info_schema(self, tracking: ConsumptionTracking) -> PrepaidInfoSchema:
         """
         Build prepaid info schema (PrepaidInfoSchema).

         Args:
             tracking: tracking consumption.

         Returns:
             PrepaidInfoSchema
         """
         total_amount_ht = self.pricingService.get_prepaid_unit_price(tracking.infos['power_recharged']) * tracking.infos['power_recharged']
         total_amount_ttc = total_amount_ht + total_amount_ht * 0.18
         return PrepaidInfoSchema(
            contract_number = tracking.infos['contract_number'],
            customer_number = "",
            invoice_date = datetime.now().strftime("%Y-%m-%d"),
            total_amount_ht = total_amount_ht,
            total_amount_ttc = total_amount_ttc,
            amount_paid = total_amount_ttc,
            power_recharged = tracking.infos['power_recharged'],
            last_power_recharged = tracking.infos['last_power_recharged'],
            total_power_recharged = tracking.infos['total_power_recharged'],
            details = []
        )


    def create_prepaid_invoices(self, tracking_number_list: list[str]) -> List[str]:
        """
         Prepaid invoice creation.

         Args:
             tracking_number_list: the list of tracking number to create.

         Returns:
             List[str]: the list of created number.
         """
        invoices: List[Invoice] = []
        created_number_list: [str] = []

        for tracking_number in tracking_number_list:
            tracking = self.prepaidTrackingService.get_invoiced_prepaid_tracking_by_number(tracking_number)
            if tracking:
                invoice = Invoice(
                    tracking_id = tracking.id,
                    invoice_number = UtilsService.generate_uuid(),
                    infos = jsonable_encoder(self.build_prepaid_info_schema(tracking))
                )
                invoices.append(invoice)
                created_number_list.append(tracking_number)

        if not invoices:
                ExceptionService.tracking_not_found()

        self.invoiceRepository.create_invoices(invoices) # create invoices
        return created_number_list # return created list numbers


    def delete_prepaid_invoice_by_number(self, invoice_number: str)-> None:
        """
        Delete prepaid invoice by number.

        Args:
            invoice_number: the invoice number.

        Returns:
            None.
        """
        self._delete_invoice(UtilsService.PREPAID, invoice_number)


    def get_prepaid_invoice_by_number(self, invoice_number: str)-> Invoice:
        """
        Get prepaid invoice by number.

        Args:
            invoice_number: the invoice number.

        Returns:
            Invoice
        """
        return self._get_invoice_by_number(UtilsService.PREPAID, invoice_number)


    def get_prepaid_invoice_by_contract_number(self, contract_number: str, offset: int, limit: int)-> List[Invoice]:
        """
        Get prepaid invoice by contract number.

        Args:
            contract_number: the contract number.
            offset: the offset.
            limit: the limit.

        Returns:
            Invoice
        """
        return self._get_invoice_by_contract_number(UtilsService.PREPAID, contract_number, offset, limit)


    def get_last_prepaid_invoice_by_contract_number(self, contract_number: str)-> Invoice:
        """
        Get last prepaid invoice by contract number.

        Args:
            contract_number: the contract number.

        Returns:
           Invoice
        """
        return self._get_last_invoice_by_contract_number(UtilsService.PREPAID, contract_number)
