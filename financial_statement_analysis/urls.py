from django.urls import path
from .views import financial_statement_analysis

urlpatterns = [
    path('financial-statement-analysis/', financial_statement_analysis, name='financial_statement_analysis'),
]