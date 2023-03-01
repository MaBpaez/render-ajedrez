from django.shortcuts import render
from .models import ClubAjedrez


def schools(request):
    todos_los_clubes = ClubAjedrez.objects.all()

    return render(request, 'escuelas/school.html', {'todos_los_clubes': todos_los_clubes})
