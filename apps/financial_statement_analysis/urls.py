from django.urls import path
from .views import FinancialStatementAnalysisView

urlpatterns = [
    path('financial-statement-analysis/', FinancialStatementAnalysisView.as_view(), name='financial-statement-analysis'),
]