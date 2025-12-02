from rest_framework import status

from .base import BaseAPITestCase
from ..models import Transaction
from django.conf import settings


class TransactionListTest(BaseAPITestCase):
    """Testes para listagem de transações."""
    
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
        
    def test_list_all_transactions(self):
        """Teste para listar todas as transações"""
        
        response = self.client.get("/transactions/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
    def test_pagination(self):
        """Teste para paginação da listagem de transações"""
        
        for i in range(7):
            Transaction.objects.create(
                description=f"T{i}",
                amount=100,
                type="income",
                date="2025-12-01",
                user=self.user
            )
        
        response = self.client.get("/transactions/?page=1")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]), 
            settings.REST_FRAMEWORK['PAGE_SIZE']
        )
        
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        
        self.assertEqual(response.data["count"], 9) # 7 criados nesse teste + 2 do setUp
        self.assertIsNotNone(response.data["next"])
        self.assertIsNone(response.data["previous"])

        # agora testar página 2
        response_page2 = self.client.get("/transactions/?page=2")

        self.assertEqual(response_page2.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response_page2.data["results"]), 
            9 - settings.REST_FRAMEWORK['PAGE_SIZE']
        )
        self.assertIsNone(response_page2.data["next"])
        self.assertIsNotNone(response_page2.data["previous"])
        
    def test_filter_transactions_by_type(self):
        """Teste para filtrar transações por tipo"""
        
        response = self.client.get("/transactions/?type=income")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['description'], "Salario")
        
    def test_filter_transactions_by_description(self):
        """Teste para filtrar transações por descricação"""
        
        response = self.client.get("/transactions/?description=Flix") # testa o case-insentive
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['description'], "Netflix")
        
    def test_filter_combined(self):
        """Teste para filtrar transações combinando os filtros"""
        
        response = self.client.get("/transactions/?type=income&description=Salario")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['description'], "Salario")
        
        response = self.client.get("/transactions/?type=expense&description=Salario")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0) # Salário não é expense, logo, será vazio