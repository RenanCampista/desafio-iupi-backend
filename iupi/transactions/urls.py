from rest_framework import routers
from django.urls import path
from .views import TransactionViewSet, SummaryView

router = routers.DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('summary/', SummaryView.as_view(), name='summary'),
] + router.urls
