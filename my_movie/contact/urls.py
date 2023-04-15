from django.urls import path
from .views import create_contact

urlpatterns = [
    path('', create_contact, name='contact'),

]