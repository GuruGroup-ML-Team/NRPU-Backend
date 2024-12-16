from django.urls import path
from .views import AltmanZScoreView

urlpatterns = [
        path('altman-zscore/', AltmanZScoreView.as_view(), name='altman-zscore'),
]