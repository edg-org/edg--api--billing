from fastapi import Depends
from typing import List, Optional
from pydantic import parse_obj_as
from datetime import datetime, date
from api.models.Invoice import Invoice
from fastapi.encoders import jsonable_encoder
from api.services.UtilsService import UtilsService
from api.services.InvoiceService import InvoiceService
from api.services.PricingService import PricingService
from api.services.ExceptionService import ExceptionService
from api.models.ConsumptionTracking import ConsumptionTracking
from api.repositories.InvoiceRepository import InvoiceRepository
from api.schemas.InvoiceSchema import PostpaidInfoSchema, Dunning
from api.services.PostpaidTrackingService import PostpaidTrackingService

class PostpaidInvoiceService(InvoiceService):
    invoiceRepository: InvoiceRepository
    postpaidTrackingService: PostpaidTrackingService
    pricingService: PricingService

    def __init__(
            self,
            invoiceRepository: InvoiceRepository = Depends(),
            postpaidTrackingService: PostpaidTrackingService = Depends(),
            pricingService: PricingService = Depends()
    ) -> None:
        super().__init__(invoiceRepository)
        self.invoiceRepository = invoiceRepository
        self.postpaidTrackingService = postpaidTrackingService
        self.pricingService = pricingService


    @staticmethod
    def build_dunning(name: str = "notification", last_dunning: Dunning = None, delay_penalty_rate = 0.00) -> Dunning:
        """
        Build dunning.

        Args:
            name: the dunning name.
            last_dunning: the las dunning.
            delay_penalty_rate: the delay penalty rate.

        Returns:
            Dunning
        """
        return Dunning(
            name = name,
            rank = 0 if last_dunning is None else last_dunning.rank + 1,
            date = datetime.now().strftime("%Y-%m-%d"),
            delay_penalty_rate = 0.00 if last_dunning is None else last_dunning.delay_penalty_rate + delay_penalty_rate,
            total_amount_ht = 0.00, # default value
            total_amount_ttc = 0.00, # default value
            payment_deadline = 0 # default value
        )


    def build_postpaid_info_schema(self, tracking: ConsumptionTracking) -> PostpaidInfoSchema:
         """
         Build postpaid info schema (PostpaidInfoSchema).

         Args:
             tracking: tracking consumption.

         Returns:
             PostpaidInfoSchema
         """
         total_amount_ht = self.pricingService.get_postpaid_unit_price(tracking.infos['index_value']) * tracking.infos['index_value']
         total_amount_ttc = total_amount_ht * (1 + UtilsService.VAT)
         dunning = self.build_dunning()
         dunning.total_amount_ht = total_amount_ht
         dunning.total_amount_ttc = total_amount_ttc
         dunning.payment_deadline = UtilsService.MONTHLY
         return PostpaidInfoSchema(
            contract_number = tracking.infos['contract_number'],
            customer_number = "",
            invoice_date = datetime.now().strftime("%Y-%m-%d"),
            index_value = tracking.infos['index_value'],
            total_amount_ht = total_amount_ht,
            total_amount_ttc = total_amount_ttc,
            amount_paid = 0.00,
            last_index_value = tracking.infos['last_index_value'],
            total_power_consumed = tracking.infos['total_power_consumed'],
            remaining_amount = total_amount_ttc,
            previous_status = "",
            payment_deadline = UtilsService.MONTHLY,
            invoicing_frequency = 1,
            deadline_measurement_unit = "day",
            details = [],
            dunning_max = 2,
            dunning = [dunning]
        )

    def create_postpaid_invoices(self, tracking_number_list: list[str]) -> List[str]:
        """
         Postpaid invoice creation.

         Args:
             tracking_number_list: the list of tracking number to create.

         Returns:
             List[str]: the list of created number.
         """
        invoices: List[Invoice] = []
        created_number_list: [str] = []
        tracking_list: [ConsumptionTracking] = []

        for tracking_number in tracking_number_list:
            tracking = self.postpaidTrackingService.get_not_invoiced_postpaid_tracking_by_number(tracking_number) # get a postpaid tracking by tracking_number
            if tracking:
                invoice = Invoice(
                    tracking_id = tracking.id,
                    invoice_number = UtilsService.generate_uuid(),
                    invoice_date = datetime.now(),
                    infos = jsonable_encoder(self.build_postpaid_info_schema(tracking))
                )
                invoices.append(invoice)
                created_number_list.append(tracking_number)
                tracking_list.append(tracking)

        if not invoices:
                ExceptionService.tracking_not_found()

        self.invoiceRepository.create_invoices(invoices) # create invoices
        self.postpaidTrackingService.update_postpaid_tracking(tracking_list) # update postpaid tracking
        return created_number_list # return created list numbers


    def delete_postpaid_invoice_by_number(self, invoice_number: str)-> None:
        """
        Delete postpaid invoice by number.

        Args:
            invoice_number: the invoice number.

        Returns:
            None.
        """
        self._delete_invoice(UtilsService.POSTPAID, invoice_number)

    def get_postpaid_invoice_by_number(self, invoice_number: str)-> Invoice:
        """
        Get postpaid invoice by number.

        Args:
            invoice_number: the invoice number.

        Returns:
            Invoice
        """
        return self._get_invoice_by_number(UtilsService.POSTPAID, invoice_number)

    def _update_invoice_for_new_dunning(self, invoice: Invoice, infos: PostpaidInfoSchema, new_dunning: Dunning) -> None:
         """
         Update invoice for the new dunning.

         Args:
             invoice: the invoice to update.
             infos: the invoice infos.
             new_dunning: the new dunning.

         Returns:
             None
         """
         infos.dunning.append(new_dunning) # append new dunning to the dunning list
         infos.payment_deadline = new_dunning.payment_deadline
         infos.total_amount_ht += 0.00 if new_dunning.delay_penalty_rate == 0.00 else infos.total_amount_ht * new_dunning.delay_penalty_rate
         infos.total_amount_ttc = infos.remaining_amount = infos.total_amount_ht * (1 + UtilsService.VAT)
         invoice.infos = jsonable_encoder(infos)
         invoice.updated_at = datetime.now()
         self.invoiceRepository.update_invoice(invoice) # update invoice

    def dunning_postpaid_invoice_by_number(self, invoice_number: str)-> None:
        """
         Dunning postpaid invoice by number.

         Args:
             invoice_number: the invoice number.

         Returns:
             None
        """
        invoice = self.get_postpaid_invoice_by_number(invoice_number) # get an invoice by invoice_number
        if not invoice:
            ExceptionService.invoice_not_found()

        infos = parse_obj_as(PostpaidInfoSchema, invoice.infos)
        last_rank = max([dunning.rank for dunning in infos.dunning]) # get the max of ranks from the dunning list
        last_dunning = [dunning for dunning in infos.dunning if dunning.rank == last_rank][-1]
        days = (date.today() - datetime.strptime(last_dunning.date, "%Y-%m-%d").date()).days # days since invoice generated
        infos.previous_status = last_dunning.name if last_rank == 0 else last_dunning.name + " " + str(last_rank)
        infos.payment_deadline -=  days

        if last_rank < infos.dunning_max: # generate new dunning without applying penalty
            new_dunning = self.build_dunning("dunning", last_dunning) # build the dunning
            new_dunning.total_amount_ht = last_dunning.total_amount_ht
            new_dunning.total_amount_ttc = last_dunning.total_amount_ttc
            new_dunning.payment_deadline = infos.payment_deadline
            self._update_invoice_for_new_dunning(invoice, infos, new_dunning) # update invoice for the new dunning
        else: #generate new dunning with applying penalty
            new_dunning = self.build_dunning("dunning", last_dunning, 0.01) # build the dunning
            new_dunning.total_amount_ht = last_dunning.total_amount_ht * (1 + new_dunning.delay_penalty_rate)
            new_dunning.total_amount_ttc = new_dunning.total_amount_ht * (1 + UtilsService.VAT)
            new_dunning.payment_deadline = infos.payment_deadline
            self._update_invoice_for_new_dunning(invoice, infos, new_dunning) # update invoice for the new dunning

    def get_postpaid_invoice_by_contract_number(self, contract_number: str, offset: int, limit: int)-> List[Invoice]:
        """
        Get postpaid invoice by contract number.

        Args:
            contract_number: the contract number.
            offset: the offset.
            limit: the limit.

        Returns:
            List[Invoice]
        """
        return self._get_invoice_by_contract_number(UtilsService.POSTPAID, contract_number, offset, limit)


    def get_last_postpaid_invoice_by_contract_number(self, contract_number: str)-> Invoice:
        """
        Get last postpaid invoice by contract number.

        Args:
            contract_number: the contract number.

        Returns:
           Invoice
        """
        return self._get_last_invoice_by_contract_number(UtilsService.POSTPAID, contract_number)
