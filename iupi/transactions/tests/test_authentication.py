from rest_framework import status

from .base import BaseAPITestCase


class AuthenticationTest(BaseAPITestCase):
    """Testes para autenticação das rotas protegidas"""

    def test_cannot_access_transactions_without_token(self):
        """Sem token deve retornar 401"""

        response = self.client.get("/transactions/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
