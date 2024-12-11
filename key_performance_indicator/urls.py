from django.urls import path
from .views import key_performance_indicator

urlpatterns = [
    path('Key-Performance-Indicator/', key_performance_indicator, name='key_performance_indicator'),

]