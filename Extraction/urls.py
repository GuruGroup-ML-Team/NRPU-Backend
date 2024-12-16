from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.calculating.urls')),  # Include calculations app URLs
    path('api/', include('apps.economic_data.urls')),
    path('api/', include('apps.financial_statement_analysis.urls')),
    path('api/', include('apps.key_performance_indicator.urls')),
    path('api/', include('apps.altman_z_score.urls')),
    path('api/', include('apps.generalized_method_of_moment.urls')),

]