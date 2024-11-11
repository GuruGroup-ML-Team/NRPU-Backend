from django.urls import path
from . import views

urlpatterns = [
    path('financial/', views.financial_market_data, name='financial_market_data'),
]
