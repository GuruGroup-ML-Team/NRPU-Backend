# indicators/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('economic-data/', views.economic_data, name='economic-data-api'),
]
