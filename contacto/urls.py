from django.urls import path
from . import views

app_name = 'contacto'

urlpatterns = [
    # Path de contacto
    path('', views.contact, name='contact'),
]
