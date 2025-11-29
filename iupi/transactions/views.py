from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar transações financeiras."""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        """Busca transações com base em filtros opcionais de descrição e tipo.

        Returns:
            _type_: QuerySet de transações filtradas.
        """
        
        queryset = Transaction.objects.all()
        
        description = self.request.query_params.get('description')
        type = self.request.query_params.get('type')
        
        if description:
            queryset = queryset.filter(description__icontains=description)
            
        if type:
            queryset = queryset.filter(type=type)
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def summary(self, request) -> Response:
        """Retorna um resumo das transações, incluindo totais de receitas, despesas e saldo.

        Args:
            request (_type_): Requisição HTTP.
        Returns:
            Response: Resposta HTTP com o resumo das transações.
        """
        total_income = Transaction.objects.filter(type="income").aggregate(total=Sum('amount'))['total'] or 0
        total_expense = Transaction.objects.filter(type="expense").aggregate(total=Sum('amount'))['total'] or 0
        
        summary_data = {
            "total_income": f"{total_income:.2f}",
            "total_expense": f"{total_expense:.2f}",
            "net_balance": f"{total_income - total_expense:.2f}"
        }
        
        return Response(summary_data)
    