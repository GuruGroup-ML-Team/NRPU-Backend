# indicators/urls.py
from django.urls import path
from .views import EconomicDataView

urlpatterns = [
    path('economic-data/', EconomicDataView.as_view(), name='economic-data'),
]
