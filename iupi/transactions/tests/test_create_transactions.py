from rest_framework import status

from .base import BaseAPITestCase
from ..models import Transaction


class TransactionCreateTest(BaseAPITestCase):
    """Testes criação de transações."""

    def setUp(self):
        super().setUp()
        self.authenticate()

    def test_create_transaction(self):
        """Teste para criar uma transação com dados válidos."""

        payload = {
            "description": "Salario",
            "amount": 1000,
            "type": "income",
            "date": "2025-11-28"
        }

        response = self.client.post("/api/transactions/", payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)

        transaction = Transaction.objects.first()
        self.assertEqual(transaction.user, self.user)

    def test_create_incomplete_transaction(self):
        """Teste para criar uma transação com dados incompletos"""
        
        payload = {
            "amount": 1000,
            "type": "income",
            "date": "2025-11-28"
        }
        
        response = self.client.post("/api/transactions/", payload)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("description", response.data)
        
    def test_create_invalid_type_transaction(self):
        """Teste para criar uma transação de tipo inválido"""
        
        payload = {
            "description": "Salario",
            "amount": 1000,
            "type": "renda",
            "date": "2025-11-28"
        }
        
        response = self.client.post("/api/transactions/", payload)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("type", response.data)