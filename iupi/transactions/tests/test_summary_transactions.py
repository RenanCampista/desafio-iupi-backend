from rest_framework import status

from .base import BaseAPITestCase
from ..models import Transaction


class TransactionSummaryTest(BaseAPITestCase):
    """"Testes para resumo de transações."""
    def setUp(self):
        super().setUp()
        self.authenticate()
        
        Transaction.objects.create(
            description="Salario",
            amount=2000,
            type="income",
            date="2025-12-01",
            user=self.user
        )

        Transaction.objects.create(
            description="Netflix",
            amount=50,
            type="expense",
            date="2025-12-01",
            user=self.user
        )
        
    def test_summary_transactions(self):
        """Teste para obter o resumo das transações"""
        response = self.client.get("/summary/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_income'], '2000.00')
        self.assertEqual(response.data['total_expense'], '50.00')
        self.assertEqual(response.data['net_balance'], '1950.00')