# calculations/urls.py
from django.urls import path
from .views import calculate_indicator

urlpatterns = [
    path('', calculate_indicator, name='calculate_indicator'),
]