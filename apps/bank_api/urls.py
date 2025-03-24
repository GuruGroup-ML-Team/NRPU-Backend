from django.urls import path
from .views import CreditRiskAPIView

urlpatterns = [
    path('credit-risk/', CreditRiskAPIView.as_view(), name='credit-risk'),
]