# project_root/credit_risk/urls.py

from django.urls import path
# Import views from previous logic files
from .views.organization_data_view import FetchSpecificOrgDataView, FetchSectorDataView
from .views.financial_variables_view import OrgSpecificFinancialVariablesView, SectorAverageFinancialVariablesView
from .views.ratio_comparison_view import RatioComparisonView
# Corrected import for Financial Ratios views (Logic Three)
from .views.financial_ratios_view import CompanyRatiosView, SectorRatiosView
# Import views from the new logic file (overall_score_views)
from .views.overall_score_view import OverallScoreView

urlpatterns = [
    # Endpoints for Organization Data (Logic One)
    path('credit-risk/organization/fetch-specific-org/', FetchSpecificOrgDataView.as_view(), name='fetch_specific_org_data'),
    path('credit-risk/organization/fetch-by-sector/', FetchSectorDataView.as_view(), name='fetch_by_sector_data'),

    # Endpoints for Financial Variables (Logic Two)
    path('credit-risk/financial-variables/org-specific/', OrgSpecificFinancialVariablesView.as_view(), name='org_specific_financial_variables'),
    path('credit-risk/financial-variables/sector-average/', SectorAverageFinancialVariablesView.as_view(), name='sector_average_financial_variables'),

    # Endpoints for Financial Ratios (Logic Three)
    path('credit-risk/financial-ratios/company-ratios/', CompanyRatiosView.as_view(), name='company_ratios'),
    path('credit-risk/financial-ratios/sector-ratios/', SectorRatiosView.as_view(), name='sector_ratios'),

    # Endpoints for Ratio Comparison (Logic Four)
    path('credit-risk/ratio-comparison/compare-ratios/', RatioComparisonView.as_view(), name='compare_ratios'),

    # Endpoints for Overall Score (Logic Five)
    path('credit-risk/overall-score/calculate/', OverallScoreView.as_view(), name='calculate_overall_score'),
]
