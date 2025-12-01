from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(ModelViewSet):
    """ViewSet para gerenciar transações financeiras."""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated] # Exige autenticação para acessar as rotas

    def get_queryset(self):
        """Busca transações com base em filtros opcionais de descrição e tipo.

        Returns:
            _type_: QuerySet de transações filtradas.
        """
        
        queryset = Transaction.objects.filter(user=self.request.user)
        
        description = self.request.query_params.get('description')
        type = self.request.query_params.get('type')
        
        if description:
            queryset = queryset.filter(description__icontains=description)
            
        if type:
            queryset = queryset.filter(type=type)
            
        return queryset.order_by('-date')
    
    def perform_create(self, serializer: TransactionSerializer):
        """Associa o usuário autenticado à transação ao criá-la.

        Args:
            serializer (TransactionSerializer): Serializador da transação.
        """
        serializer.save(user=self.request.user)
    
    
class SummaryView(APIView):
    """View para retornar resumo das transações."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request: Request) -> Response:
        """Retorna um resumo das transações, incluindo totais de receitas, despesas e saldo.

        Args:
            request (Request): Requisição HTTP.
        Returns:
            Response: Resposta HTTP com o resumo das transações.
        """
        total_income = Transaction.objects.filter(
            user=self.request.user, type="income"
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        total_expense = Transaction.objects.filter(
            user=self.request.user, type="expense"
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        summary_data = {
            "total_income": f"{total_income:.2f}",
            "total_expense": f"{total_expense:.2f}",
            "net_balance": f"{total_income - total_expense:.2f}"
        }
        
        return Response(summary_data)
    