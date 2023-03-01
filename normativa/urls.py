from django.urls import path
from . import views

app_name = "normativa"

urlpatterns = [
    # Path todas las circulares año en curso
    path("", views.circular, name="circulares"),
    # Path Buscar, importante que vaya en primer lugar, sino no funcionará
    path("search/", views.circular_search, name="circular_search"),
    # Path todas las circulares
    path("<slug:todas_circulares>/", views.circular, name="todas-circulares"),
    # Path circulares año y mes
    path(
        "circulares/<int:year>/<int:month>/",
        views.circular,
        name="circulares-year-month",
    ),
]
