from django.urls import path
from .views import GeneralizedMethodOfMoment

urlpatterns = [
    path('Generalized-Method-Of-Moment/', GeneralizedMethodOfMoment.as_view(), name='GeneralizedMethodOfMoment'),
]