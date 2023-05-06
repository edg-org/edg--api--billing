from typing import List

from fastapi import APIRouter, Depends, status

from api.services.PostpaidInvoiceService import PostpaidInvoiceService

PostpaidInvoiceRouter = APIRouter(prefix="/invoices/postpaid", tags=["postpaid invoices"])

@PostpaidInvoiceRouter.post(
    "/",
    status_code = status.HTTP_201_CREATED,
    summary = "Create postpaid invoice",
    description = "Create postpaid invoice on bulk depending on the list of tracking number"
)
def create_postpaid_invoices(
    tracking_number_list: list[str],
    postpaidInvoiceService: PostpaidInvoiceService = Depends()
):
    return postpaidInvoiceService.create_postpaid_invoices(tracking_number_list)


@PostpaidInvoiceRouter.get(
    "/number",
    summary = "Get postpaid invoice by number",
    description = "Get postpaid invoice with the tracking number"
)
def get_postpaid_invoice_by_number(
    invoice_number: str,
    postpaidInvoiceService: PostpaidInvoiceService = Depends()
):
    return postpaidInvoiceService.get_postpaid_invoice_by_number(invoice_number)


@PostpaidInvoiceRouter.get(
    "/contract_number",
    summary = "Get postpaid invoice by contract number",
    description = "Get postpaid invoice with the contract number"
)
def get_postpaid_invoices_by_contract_number(
    contract_number: str,
    offset: int = 0,
    limit: int = 10,
    postpaidInvoiceService: PostpaidInvoiceService = Depends()
):
    return postpaidInvoiceService.get_postpaid_invoice_by_contract_number(contract_number, offset, limit)


@PostpaidInvoiceRouter.get(
    "/contract_number/last",
    summary = "Get last postpaid invoice by contract number",
    description = "Get last postpaid invoice with the contract number"
)
def get_last_postpaid_invoice_by_contract_number(
    contract_number: str,
    postpaidInvoiceService: PostpaidInvoiceService = Depends()
):
    return postpaidInvoiceService.get_last_postpaid_invoice_by_contract_number(contract_number)


@PostpaidInvoiceRouter.get(
    "/dunning",
    summary = "Dunning postpaid invoice by invoice number",
    description = "Dunning postpaid invoice with the invoice number"
)
def dunning_postpaid_invoice_by_number(
    invoice_number: str,
    postpaidInvoiceService: PostpaidInvoiceService = Depends()
):
    return postpaidInvoiceService.dunning_postpaid_invoice_by_number(invoice_number)


@PostpaidInvoiceRouter.delete(
    "/number",
    summary = "Delete postpaid invoice by number",
    description = "Delete postpaid invoice with the invoice number"
)
def delete_postpaid_invoice_by_number(
    invoice_number: str,
    postpaidInvoiceService: PostpaidInvoiceService = Depends()
):
    postpaidInvoiceService.delete_postpaid_invoice_by_number(invoice_number)
