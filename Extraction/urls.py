from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('calculating.urls')),  # Include calculations app URLs
    path('api/', include('financial_market_data.urls')),
    path('api/', include('Economic_Data.urls')),

]