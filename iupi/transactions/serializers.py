from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Transaction."""
    
    class Meta:
        model = Transaction
        fields = [
            'id',
            'description',
            'amount',
            'type',
            'date',
            'user',
        ]
        
    def validate_amount(self, value: float) -> float:
        """Valida o campo 'amount'.
        Garante que o valor seja maior que zero.

        Args:
            value (float): valor recebido no request.

        Returns:
            float: O mesmo valor caso seja válido.
            
        Raises:
            serializers.ValidationError: Se o valor for menor ou igual a zero.
        """
        if value <= 0:
            raise serializers.ValidationError("Amount deve ser maior que zero.")
        return value
    
    def validate_type(self, value: str) -> str:
        """Valida o campo 'type'.
        Garante que o valor seja 'income' ou 'expense'.

        Args:
            value (str): valor recebido no request.

        Returns:
            str: O mesmo valor caso seja válido.
            
        Raises:
            serializers.ValidationError: Se o valor não for 'income' ou 'expense'.
        """
        if value not in ['income', 'expense']:
            raise serializers.ValidationError("Type deve ser 'income' ou 'expense'.")
        return value