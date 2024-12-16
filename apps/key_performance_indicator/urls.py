from django.urls import path
from .views import KeyPerformanceIndicatorView

urlpatterns = [
    path('key-performance-indicator/', KeyPerformanceIndicatorView.as_view(), name='key_performance_indicator'),

]