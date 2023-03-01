from django.urls import path
from . import views

app_name = 'page'

urlpatterns = [
    # Path PAGE
    path('<int:page_id>/<slug:page_title>/', views.page, name='page'),
]
