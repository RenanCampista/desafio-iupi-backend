from django.db import models
from django.contrib.auth.models import User


class Transaction(models.Model):
    """Modelo para representar uma transação financeira."""
    TYPE_CHOICES = [
        ("income", "Income"),
        ("expense", "Expense"),
    ]
    
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    date = models.DateField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="transactions",
        null=True, # Deixar null até que a autenticação esteja implementada
        blank=True
    )
    
    def __str__(self):
        return f"{self.description} - {self.amount} ({self.type})"