import requests
import datetime
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mass_mail
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import TorneoDiputacion, RegistrationTournamentDiputacion
from .forms import RegistrationTournamentDiputacionForm, LowInTournamentDiputacionForm, SearchForm
from .tasks import register_created, low_created


def circuito_torneos_list(request, tipo_torneo=None, all_tournaments=None, in_progress=None, finished=None):

    form_search = SearchForm()
    current_month = timezone.now().strftime("%m")
    torneos_mes_actual = TorneoDiputacion.objects.filter(start__month=int(current_month))

    # utilizamos date para comprobar solo fechas con el formato Y-m-d
    # Refe:https://docs.djangoproject.com/en/3.2/ref/models/querysets/#date

    # Por defecto se muestran los torneos nuevos
    object_list = TorneoDiputacion.objects.filter(
            start__date__gt=timezone.now().strftime("%Y-%m-%d")
    )

    if all_tournaments:
        print(all_tournaments, "Solicita todos los torneos")
        object_list = TorneoDiputacion.objects.all()

    if in_progress:
        print(in_progress, "Solicita torneos en progreso")
        object_list = TorneoDiputacion.objects.filter(
            start__date__lte=timezone.now().strftime("%Y-%m-%d"),
            finish__date__gte=timezone.now().strftime("%Y-%m-%d"),
        )

    if finished:
        print(finished, "Solicita torneos finalizados")
        object_list = TorneoDiputacion.objects.filter(
            finish__date__lt=timezone.now().strftime("%Y-%m-%d")
        )

    paginator = Paginator(object_list, 10)  # torneos(objects) in each page
    page = request.GET.get("page")

    try:
        torneos = paginator.page(page)  # todos los objetos de una página

    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        torneos = paginator.page(1)

    except EmptyPage:
        # if pages is out of range deliver las page of results
        torneos = paginator.page(paginator.num_pages)

    return render(
        request,
        "circuitos/circuitos_list.html",
        {
            'torneos': torneos,
            'form': form_search,
            'tipo_torneo': tipo_torneo,
            'torneos_mes_actual': torneos_mes_actual
        }
    )


def circuito_torneo_detail(request, year, month, day, torneo):
    torneo = get_object_or_404(
        TorneoDiputacion, slug=torneo, publish__year=year, publish__month=month, publish__day=day
    )
    allow_registration = False
    submitted_form = False

    if not torneo.quantity and not torneo.registre:  # organiza delegación y no aforo
        allow_registration = False
    elif timezone.now().strftime("%Y-%m-%d") >= torneo.end_registration.strftime(
        "%Y-%m-%d"
    ):  # para todos organize quien organize
        allow_registration = False
    elif torneo.quantity and not torneo.registre:  # organiza delegación y hay aforo
        allow_registration = True
    elif not torneo.quantity and torneo.registre:
        # organiza 3 parte y fecha actual < fecha fin registro
        allow_registration = True

    form = RegistrationTournamentDiputacionForm()
    low_form = LowInTournamentDiputacionForm()

    if request.method == "POST":
        if "low" in request.POST:
            low_form = LowInTournamentDiputacionForm(request.POST)
            form = RegistrationTournamentDiputacionForm()

            if low_form.is_valid():
                """reCAPTCHA validation"""
                recaptcha_response = request.POST.get("g-recaptcha-response")
                data = {
                    "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                    "response": recaptcha_response,
                }
                r = requests.post(
                    "https://www.google.com/recaptcha/api/siteverify", data=data
                )
                result = r.json()

                print(result)

                """ if reCAPTCHA returns True """
                if result["success"]:
                    # diccionario datos limpios del formulario de baja
                    cd = low_form.cleaned_data
                    try:
                        registration = RegistrationTournamentDiputacion.objects.get(
                            name=cd["name"],
                            surnames=cd["surnames"],
                            mail=cd["mail"],
                            tournament_title=request.POST.get("tournament_title"),
                        )
                        registration.delete()
                        messages.info(request, "Baja realizada con éxito.")
                        torneo.quantity = torneo.quantity + 1  # update
                        torneo.save()
                        
                        low_created.delay(cd, torneo.title)
                        # message1 = (
                        #     "Baja en torneo",
                        #     f"Enhorabuena {cd['name']} te has dado de baja en el torneo {torneo.title}",
                        #     "info@ajedrezmalaga.org",
                        #     [f"{cd['mail']}"],
                        # )
                        # message2 = (
                        #     "Baja en torneo",
                        #     f"{cd['name']} {cd['surnames']} se ha dado de baja en el torneo {torneo.title}",
                        #     "info@ajedrezmalaga.org",
                        #     ["admin@ajedrezmalaga.org"],
                        # )

                        # send_mass_mail((message1, message2), fail_silently=False)
                        low_form = LowInTournamentDiputacionForm()
                    except ObjectDoesNotExist:
                        messages.error(request, "El usuario no está registrado.")

        elif not "low" in request.POST:
            print(request.POST)
            form = RegistrationTournamentDiputacionForm(request.POST)
            low_form = LowInTournamentDiputacionForm()

            if form.is_valid():
                """reCAPTCHA validation"""
                recaptcha_response = request.POST.get("g-recaptcha-response")
                data = {
                    "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                    "response": recaptcha_response,
                }
                r = requests.post(
                    "https://www.google.com/recaptcha/api/siteverify", data=data
                )
                result = r.json()

                print(result)

                """ if reCAPTCHA returns True """
                if result["success"]:
                    print("FORMULARIO ENVIADO CON EXITO")
                    new_tournamentregistration = form.save(commit=False)
                    new_tournamentregistration.tournament = torneo
                    # new_tournamentregistration.status = request.POST.get('status')
                    new_tournamentregistration.save()

                    torneo.quantity = torneo.quantity - 1  # update
                    torneo.save()
                    # print('Torneo despues de grabar', torneo.quantity)

                    # envio correo electronico a la delegación y al registrado
                    # para ello utilizaremos send_mass_mail()
                    # https://docs.djangoproject.com/en/3.2/topics/email/#send-mass-mail
                    cd = form.cleaned_data

                    register_created.delay(cd, torneo.title)
                    # message1 = (
                    #     "Inscripción en torneo",
                    #     f"Enhorabuena {cd['name']} te has registrado en el torneo {torneo.title}",
                    #     "info@ajedrezmalaga.org",
                    #     [f"{cd['mail']}"],
                    # )
                    # message2 = (
                    #     "Inscripción en torneo",
                    #     f"{cd['name']} {cd['surnames']} se ha registrado en el torneo {torneo.title}",
                    #     "info@ajedrezmalaga.org",
                    #     ["admin@ajedrezmalaga.org"],
                    # )

                    # send_mass_mail((message1, message2), fail_silently=False)

                    submitted_form = True
                    form = RegistrationTournamentDiputacionForm()  # borrar campos crear form nuevo

    # else:
    #     form = RegistrationTournamentDiputacionForm()
    #     low_form = LowInTournamentDiputacionForm()

    return render(
        request,
        "circuitos/circuito_detail.html",
        {
            "torneo": torneo,
            "allow_registration": allow_registration,
            "recaptcha_site_key": settings.GOOGLE_RECAPTCHA_SITE_KEY,
            "form": form,
            "submitted_form": submitted_form,
            "low_form": low_form,
        },
    )


def circuito_search(request):
    form = SearchForm()
    query = None
    results = []

    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            # Búsqueda
            results = set(
                TorneoDiputacion.objects.filter(
                    Q(title__icontains=query)
                    | Q(location__icontains=query)
                    | Q(body__icontains=query)
                    | Q(province__icontains=query)
                )
            )
            print(results)

    return render(
        request,
        "circuitos/search.html",
        {"query": query, "form": form, "results": results},
    )


def historico_torneos_diputacion(request, year=None, month=None, all_tournaments=None):
    '''Vamos a obtener los torneos de los dos años anteriores al año en curso, los
    torneos del año en curso y los torneos de un año y un mes'''

    year_month_tournaments = False
    get_all_tournaments = False
    qs = False
    formatted_date = ''
    before_last_year = str(int(timezone.now().strftime("%Y")) - 2)
    last_year = str(int(timezone.now().strftime("%Y")) - 1)
    current_year = timezone.now().strftime("%Y")
    form_search = SearchForm()

    object_list = TorneoDiputacion.objects.filter(start__year=current_year)

    if all_tournaments:
        object_list = TorneoDiputacion.objects.all()
        get_all_tournaments = True

    if year and month:
        object_list = TorneoDiputacion.objects.filter(
            start__year=int(year), start__month=int(month)
        )
        year_month_tournaments = True
        qs = True
        formatted_date = datetime.datetime(year, month, 17).strftime("%B %Y")
        print(formatted_date)

    paginator = Paginator(object_list, 10)  # torneos(objects) in each page
    page = request.GET.get("page")
    try:
        torneos = paginator.page(page)  # todos los objetos de una página

    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        torneos = paginator.page(1)

    except EmptyPage:
        # if pages is out of range deliver las page of results
        torneos = paginator.page(paginator.num_pages)


    return render(
        request,
        "circuitos/historico_circuitos_nuevo.html",
        {
            "torneos": torneos,
            'current_year': current_year,
            'last_year': last_year,
            'before_last_year': before_last_year,
            'year_month_tournaments': year_month_tournaments,
            'qs': qs,
            'formatted_date': formatted_date,
            'get_all_tournaments': get_all_tournaments,
            'form': form_search
        },
    )