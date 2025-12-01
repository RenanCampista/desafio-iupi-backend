from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class BaseAPITestCase(APITestCase):
    """Classe base para testes de API com autenticação JWT."""

    def authenticate(self):
        """Cria um usuário de teste e autentica a requisição com JWT."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + access_token
        )