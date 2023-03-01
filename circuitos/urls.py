from django.urls import path
from . import views

app_name = 'circuitos'

urlpatterns = [
    path(
        '',
        views.circuito_torneos_list,
        {'tipo_torneo': 'nuevos'},
        name='new_tournaments',
    ),
    path("search/", views.circuito_search, name="circuito_search"),
    path(
        'todos-los-torneos/',
        views.circuito_torneos_list,
        {'all_tournaments': True, 'tipo_torneo': 'todos'},
        name='all_tournaments',
    ),
    path(
        'torneos-en-curso/',
        views.circuito_torneos_list,
        {'in_progress': True, 'tipo_torneo': 'en curso'},
        name='tournaments_in_progress',
    ),
    path(
        'torneos-finalizados/',
        views.circuito_torneos_list,
        {'finished': True, 'tipo_torneo': 'finalizados'},
        name='finished_tournaments',
    ),
    path(
        '<int:year>/<int:month>/<int:day>/<slug:torneo>/',
        views.circuito_torneo_detail,
        name='circuito-detail',
    ),
    # Path torneos año en curso
    path(
        'historico-torneos/',
        views.historico_torneos_diputacion,
        name='historico-torneos-diputacion',
    ),
    # Path torneos año y mes
    path(
        'historico-torneos/<int:year>/<int:month>/',
        views.historico_torneos_diputacion,
        name='torneos-year-month',
    ),
    # Paht todos los torneos
    path(
        'historico-torneos/<slug:all_tournaments>/',
        views.historico_torneos_diputacion,
        name='todo-historico',
    ),
]
