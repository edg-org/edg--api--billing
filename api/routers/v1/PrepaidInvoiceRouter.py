from typing import List
from fastapi import APIRouter, Depends, status
from api.configs.Environment import get_env_var
from api.services.PrepaidInvoiceService import PrepaidInvoiceService

env = get_env_var()
router_path = env.api_routers_prefix + env.api_version

prepaidInvoiceRouter = APIRouter(
    prefix=router_path + "/invoices/prepaid",
    tags=["Prepaid Invoicing"],
)

@prepaidInvoiceRouter.get(
    "/{number}",
    summary = "Get prepaid invoice by number",
    description = "Get prepaid invoice with the tracking number"
)
def get_postpaid_invoice_by_number(
    number: str,
    prepaidInvoiceService: PrepaidInvoiceService = Depends()
):
    return prepaidInvoiceService.get_prepaid_invoice_by_number(number)


@prepaidInvoiceRouter.get(
    "/{contract_number}/search",
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


@prepaidInvoiceRouter.get(
    "/{contract_number}/search/last",
    summary = "Get last prepaid invoice by contract number",
    description = "Get last prepaid invoice with the contract number"
)
def get_last_prepaid_invoice_by_contract_number(
    contract_number: str,
    prepaidInvoiceService: PrepaidInvoiceService = Depends()
):
    return prepaidInvoiceService.get_last_prepaid_invoice_by_contract_number(contract_number)


@prepaidInvoiceRouter.delete(
    "/{number}",
    summary = "Delete prepaid invoice by number",
    description = "Delete prepaid invoice with the invoice number"
)
def delete_prepaid_invoice_by_number(
    number: str,
    prepaidInvoiceService: PrepaidInvoiceService = Depends()
):
    prepaidInvoiceService.delete_prepaid_invoice_by_number(number)
