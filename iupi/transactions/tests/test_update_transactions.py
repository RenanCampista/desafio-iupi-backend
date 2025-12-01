from rest_framework import status

from .base import BaseAPITestCase
from ..models import Transaction


class TransactionUpdateTest(BaseAPITestCase):
    """Testes para atualização de transações."""
    
    def setUp(self):
        super().setUp()
        self.authenticate()
        
        self.transaction =Transaction.objects.create(
            description="Salario",
            amount=2000,
            type="income",
            date="2025-12-01",
            user=self.user
        )
        
    def test_patch_update_transaction(self):
        """Teste para atualizar uma transação via PATCH."""
        
        payload = {
            "amount": 2500,
            "date": "2026-01-01"
        }
        
        response = self.client.patch(f'/transactions/{self.transaction.id}/', payload)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], "2500.00")
        self.assertEqual(response.data['date'], "2026-01-01")

        
    def test_put_update_transaction(self):
        """Teste para atualizar uma transação via PUT."""
        
        payload = {
            "description": "Salario atualizado",
            "amount": 3000,
            "type": "income",
            "date": "2026-01-01"
        }
        
        response = self.client.put(f'/transactions/{self.transaction.id}/', payload)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], "Salario atualizado")
        self.assertEqual(response.data['amount'], "3000.00")
        self.assertEqual(response.data['date'], "2026-01-01")
