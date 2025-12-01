from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient

from .base import BaseAPITestCase
from ..models import Transaction


class TransactionVisibilityTests(BaseAPITestCase):
    """Testar a visibilidade das transações."""
    
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
        
        # Simular outro cliente
        self.other_user  = User.objects.create_user(
            username='other_user',
            password='password'
        )
        
        # Precisa criar um APIClient separado
        self.client_other = APIClient()
        
        # Gera token para o outro user
        refresh = RefreshToken.for_user(self.other_user)
        access_token = str(refresh.access_token)

        self.client_other.credentials(
            HTTP_AUTHORIZATION='Bearer ' + access_token
        )

        # Transação do outro usuário
        Transaction.objects.create(
            description="Pizza",
            amount=50,
            type="expense",
            date="2025-11-28",
            user=self.other_user
        )
        
    def test_visibility_transactions(self):
        
        response = self.client.get("/transactions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["description"], "Salario")
        
        response = self.client_other.get("/transactions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["description"], "Pizza")