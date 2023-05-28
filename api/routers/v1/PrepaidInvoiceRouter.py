from typing import List
from fastapi import APIRouter, Depends, status
from api.configs.Environment import get_env_var
from api.services.PrepaidInvoiceService import PrepaidInvoiceService

env = get_env_var()
router_path = env.api_routers_prefix + env.api_version

prepaidinvoiceRouter = APIRouter(
    prefix=router_path + "/invoices/prepaid",
    tags=["Prepaid Invoicing"],
)

@prepaidinvoiceRouter.get(
    "/{number}",
    summary = "Get prepaid invoice by number",
    description = "Get prepaid invoice with the tracking number"
)
def get_postpaid_invoice_by_number(
    number: str,
    prepaidInvoiceService: PrepaidInvoiceService = Depends()
):
    return prepaidInvoiceService.get_prepaid_invoice_by_number(number)


@prepaidinvoiceRouter.get(
    "/{contract_number}",
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


@prepaidinvoiceRouter.get(
    "/{contract_number}/last",
    summary = "Get last prepaid invoice by contract number",
    description = "Get last prepaid invoice with the contract number"
)
def get_last_prepaid_invoice_by_contract_number(
    contract_number: str,
    prepaidInvoiceService: PrepaidInvoiceService = Depends()
):
    return prepaidInvoiceService.get_last_prepaid_invoice_by_contract_number(contract_number)


@prepaidinvoiceRouter.delete(
    "/{number}",
    summary = "Delete prepaid invoice by number",
    description = "Delete prepaid invoice with the invoice number"
)
def delete_prepaid_invoice_by_number(
    number: str,
    prepaidInvoiceService: PrepaidInvoiceService = Depends()
):
    prepaidInvoiceService.delete_prepaid_invoice_by_number(number)
