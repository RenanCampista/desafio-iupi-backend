from rest_framework import status

from .base import BaseAPITestCase
from ..models import Transaction


class TransactionDeleteTest(BaseAPITestCase):
    """"Testes para deletar transações"""
    def setUp(self):
        super().setUp()
        self.authenticate()

        self.transaction = Transaction.objects.create(
            description="Netflix",
            amount=50,
            type="expense",
            date="2025-12-01",
            user=self.user
        )
        
    def test_delete_transactions(self):
        """Teste para deletar uma transação"""
        
        response = self.client.delete(f"/api/transactions/{self.transaction.id}/")
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Para garantir que foi deletado, a transação não pode mais existir no banco
        self.assertFalse(
            Transaction.objects.filter(id=self.transaction.id).exists()
        )
