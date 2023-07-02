from faker import Faker
from unittest import TestCase
from sqlalchemy.orm import Session
from unittest.mock import Mock, create_autospec, patch
from api.repositories.InvoiceRepository import InvoiceRepository

class TestInvoiceRepository(TestCase):
    session: Session
    invoiceRepository: InvoiceRepository


    def setUp(self):
        super().setUp()
        self.session = create_autospec(Session)
        self.invoiceRepository = InvoiceRepository(self.session)


    @patch("api.repositories.InvoiceRepository.Invoice", autospec=True)
    def test_create(self, MockInvoice):
        fake = Faker()
        invoices_list = [
            MockInvoice(
                invoice_number=fake.random_number(),
                invoice_date=fake.date_time(),
                infos=fake.sentence()
            )
        ]

        result = self.invoiceRepository.create_invoices(invoices_list)

        self.session.add_all.assert_called_once_with(invoices_list)
        self.session.commit.assert_called_once()
        self.assertEqual(result, invoices_list)


    @patch("api.repositories.InvoiceRepository.Invoice", autospec=True)
    def test_update(self, MockInvoice):
        fake = Faker()
        data  = MockInvoice(
                invoice_number=fake.random_number(),
                invoice_date=fake.date_time(),
                infos=fake.sentence()
            )

        self.invoiceRepository.update_invoice = Mock()
        self.invoiceRepository.update_invoice(data)
        self.invoiceRepository.update_invoice.assert_called_with(data)

