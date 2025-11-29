from django.shortcuts import render
from rest_framework import viewsets
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
    