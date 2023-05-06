from typing import List

from fastapi import APIRouter, Depends, status

from api.services.PrepaidInvoiceService import PrepaidInvoiceService

PrepaidInvoiceRouter = APIRouter(prefix="/invoices/prepaid", tags=["prepaid invoices"])


@PrepaidInvoiceRouter.get(
    "/number",
    summary = "Get prepaid invoice by number",
    description = "Get prepaid invoice with the tracking number"
)
def get_postpaid_invoice_by_number(
    invoice_number: str,
    prepaidInvoiceService: PrepaidInvoiceService = Depends()
):
    return prepaidInvoiceService.get_prepaid_invoice_by_number(invoice_number)


@PrepaidInvoiceRouter.get(
    "/contract_number",
    summary = "Get prepaid invoice by contract number",
    description = "Get prepaid invoice with the contract number"
)
def get_prepaid_invoice_by_contract_number(
    contract_number: str,
    offset: int = 0,
    limit: int = 10,
    prepaidInvoiceService: PrepaidInvoiceService = Depends()
):
    return prepaidInvoiceService.get_prepaid_invoice_by_contract_number(contract_number, offset, limit)


@PrepaidInvoiceRouter.get(
    "/contract_number/last",
    summary = "Get last prepaid invoice by contract number",
    description = "Get last prepaid invoice with the contract number"
)
def get_last_prepaid_invoice_by_contract_number(
    contract_number: str,
    prepaidInvoiceService: PrepaidInvoiceService = Depends()
):
    return prepaidInvoiceService.get_last_prepaid_invoice_by_contract_number(contract_number)


@PrepaidInvoiceRouter.delete(
    "/number",
    summary = "Delete prepaid invoice by number",
    description = "Delete prepaid invoice with the invoice number"
)
def delete_prepaid_invoice_by_number(
    invoice_number: str,
    prepaidInvoiceService: PrepaidInvoiceService = Depends()
):
    prepaidInvoiceService.delete_prepaid_invoice_by_number(invoice_number)
