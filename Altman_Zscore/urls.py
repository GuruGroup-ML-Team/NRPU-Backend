from django.urls import path
from .views import Altman_Zscore

urlpatterns = [
    path('Altman-Zscore/', Altman_Zscore.as_view(), name='Altman_Zscore'),
]