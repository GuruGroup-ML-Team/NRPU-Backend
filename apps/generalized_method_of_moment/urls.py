from django.urls import path
from .views import GeneralizedMethodOfMoment

urlpatterns = [
    path('generalized-method-of-moment/', GeneralizedMethodOfMoment.as_view(), name='generalized-method-of-moment'),
]