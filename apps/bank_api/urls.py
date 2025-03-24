# from django.urls import path
# # Import bank API views
# from .views import (
#     BankListAPIView,
#     BankDetailAPIView,
#     BankComparisonAPIView,
#     BankRankingAPIView,
#     BankFinancialAnalysisAPIView,
#     SectorListAPIView,
#     SubSectorListAPIView,
#     BanksBySubSectorAPIView,
#     MetricsListAPIView,
#     YearsListAPIView,
#     BankComparativeAnalysisAPIView,
#     BankScoreAPIView,
#     BankTrendAnalysisAPIView
# )

# # Import company API views
# from .company_views import (
#     CompanyListAPIView,
#     CompanyDetailAPIView,
#     CompanyComparisonAPIView,
#     CompanyRankingAPIView,
#     CompanyFinancialAnalysisAPIView,
#     CompanySectorListAPIView,
#     CompanySubSectorListAPIView,
#     CompaniesbySubSectorAPIView,
#     CompanyIndicatorsListAPIView,
#     CompanySubIndicatorsListAPIView,
#     CompanyYearsListAPIView,
#     CompanyComparativeAnalysisAPIView,
#     CompanyScoreAPIView,
#     CompanyTrendAnalysisAPIView
# )

# # Bank API URL patterns
# urlpatterns = [
#     # Bank endpoints
#     path('banks/', BankListAPIView.as_view(), name='bank-list'),
#     path('banks/compare/', BankComparisonAPIView.as_view(), name='bank-comparison'),
#     path('banks/ranking/', BankRankingAPIView.as_view(), name='bank-ranking'),
#     path('banks/comparative-analysis/', BankComparativeAnalysisAPIView.as_view(), name='bank-comparative-analysis'),
#     path('banks/score/', BankScoreAPIView.as_view(), name='bank-score'),
#     path('banks/<str:bank_name>/', BankDetailAPIView.as_view(), name='bank-detail'),
#     path('banks/<str:bank_name>/analysis/', BankFinancialAnalysisAPIView.as_view(), name='bank-analysis'),
#     path('banks/trend-analysis/', BankTrendAnalysisAPIView.as_view(), name='bank-trend-analysis'),

#     # Banking sector taxonomy endpoints
#     path('sectors/', SectorListAPIView.as_view(), name='sector-list'),
#     path('sub-sectors/', SubSectorListAPIView.as_view(), name='sub-sector-list'),
#     path('banks-by-sub-sector/', BanksBySubSectorAPIView.as_view(), name='banks-by-sub-sector'),
#     path('metrics/', MetricsListAPIView.as_view(), name='metrics-list'),
#     path('years/', YearsListAPIView.as_view(), name='years-list'),
# ]

# # Company API URL patterns
# company_patterns = [
#     # Company endpoints
#     path('companies/', CompanyListAPIView.as_view(), name='company-list'),
#     path('companies/compare/', CompanyComparisonAPIView.as_view(), name='company-comparison'),
#     path('companies/ranking/', CompanyRankingAPIView.as_view(), name='company-ranking'),
#     path('companies/comparative-analysis/', CompanyComparativeAnalysisAPIView.as_view(),
#          name='company-comparative-analysis'),
#     path('companies/score/', CompanyScoreAPIView.as_view(), name='company-score'),
#     path('companies/<str:company_name>/', CompanyDetailAPIView.as_view(), name='company-detail'),
#     path('companies/<str:company_name>/analysis/', CompanyFinancialAnalysisAPIView.as_view(), name='company-analysis'),
#     path('companies/trend-analysis/', CompanyTrendAnalysisAPIView.as_view(), name='company-trend-analysis'),

#     # Company taxonomy endpoints
#     path('company-sectors/', CompanySectorListAPIView.as_view(), name='company-sector-list'),
#     path('company-sub-sectors/', CompanySubSectorListAPIView.as_view(), name='company-sub-sector-list'),
#     path('companies-by-sub-sector/', CompaniesbySubSectorAPIView.as_view(), name='companies-by-sub-sector'),
#     path('company-indicators/', CompanyIndicatorsListAPIView.as_view(), name='company-indicators-list'),
#     path('company-sub-indicators/', CompanySubIndicatorsListAPIView.as_view(), name='company-sub-indicators-list'),
#     path('company-years/', CompanyYearsListAPIView.as_view(), name='company-years-list'),
# ]

# # Combine patterns
# urlpatterns += company_patterns










from django.urls import path
from .views import CreditRiskAPIView

urlpatterns = [
    path('credit-risk/', CreditRiskAPIView.as_view(), name='credit-risk'),
]