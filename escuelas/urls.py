from django.urls import path
from . import views

app_name = 'escuelas'

urlpatterns = [
    path("", views.schools, name="schools"),
]
