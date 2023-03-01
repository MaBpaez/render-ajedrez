from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Path del core
    path('', views.home, name="inicio"),
    path('torneos/', views.agenda, name='agenda'),
    path(
        'torneos/<int:year>/<int:month>/<int:day>/<slug:torneo>/',
        views.torneo_detail,
        name='torneo-detail',
    ),
    # Path torneos año en curso
    path('torneos/historico-torneos/', views.historico_torneos, name='historico-torneos'),
    # Path torneos año y mes
    path(
        'torneos/historico-torneos/<int:year>/<int:month>/',
        views.historico_torneos,
        name='torneos-year-month',
    ),
    # Paht todos los torneos
    path(
        'torneos/historico-torneos/<slug:all_tournaments>/',
        views.historico_torneos,
        name='todo-historico'
    ),
]
