from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('thanks/', ThanksTemplate.as_view(), name='thanks'),
    path('form/', home, name='form'),
]