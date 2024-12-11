from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('calculating.urls')),  # Include calculations app URLs
    path('api/', include('financial_market_data.urls')),
    path('api/', include('Economic_Data.urls')),
    path('api/', include('financial_statement_analysis.urls')),
    path('api/', include('key_performance_indicator.urls')),
    path('api/', include('Altman_Zscore.urls')),
    path('api/', include('GMM.urls')),

]