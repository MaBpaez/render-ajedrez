import requests
import datetime
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mass_mail
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.conf import settings
from .models import Torneo, TournamentRegistration
from .forms import TournamentRegistrationForm, LowInTournamentForm


def home(request):

    return render(request, "core/home.html")


def agenda(request):
    """¿crear manager personalizados?"""

    # utilizamos date para comprobar solo fechas con el formato Y-m-d
    # Refe:https://docs.djangoproject.com/en/3.2/ref/models/querysets/#date

    torneos = Torneo.objects.all()
    torneos_nuevos = Torneo.objects.filter(
        start__date__gt=timezone.now().strftime("%Y-%m-%d")
    )
    torneos_curso = Torneo.objects.filter(
        start__date__lte=timezone.now().strftime("%Y-%m-%d"),
        finish__date__gte=timezone.now().strftime("%Y-%m-%d"),
    )
    torneos_finalizados = Torneo.objects.filter(
        finish__date__lt=timezone.now().strftime("%Y-%m-%d")
    )

    return render(
        request,
        "core/agenda.html",
        {
            "torneos": torneos,
            "torneos_nuevos": torneos_nuevos,
            "torneos_curso": torneos_curso,
            "torneos_finalizados": torneos_finalizados,
        },
    )


def torneo_detail(request, year, month, day, torneo):
    torneo = get_object_or_404(
        Torneo, slug=torneo, publish__year=year, publish__month=month, publish__day=day
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

    form = TournamentRegistrationForm()
    low_form = LowInTournamentForm()

    if request.method == "POST":
        if "low" in request.POST:
            low_form = LowInTournamentForm(request.POST)
            form = TournamentRegistrationForm()

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
                        registration = TournamentRegistration.objects.get(
                            name=cd["name"],
                            surnames=cd["surnames"],
                            mail=cd["mail"],
                            tournament_title=request.POST.get("tournament_title"),
                        )
                        registration.delete()
                        messages.info(request, "Baja realizada con éxito.")
                        torneo.quantity = torneo.quantity + 1  # update
                        torneo.save()
                        message1 = (
                            "Baja en torneo",
                            f"Enhorabuena {cd['name']} te has dado de baja en el torneo {torneo.title}",
                            "info@ajedrezmalaga.org",
                            [f"{cd['mail']}"],
                        )
                        message2 = (
                            "Baja en torneo",
                            f"{cd['name']} {cd['surnames']} se ha dado de baja en el torneo {torneo.title}",
                            "info@ajedrezmalaga.org",
                            ["admin@ajedrezmalaga.org"],
                        )

                        send_mass_mail((message1, message2), fail_silently=False)
                        low_form = LowInTournamentForm()
                    except ObjectDoesNotExist:
                        messages.error(request, "El usuario no está registrado.")

        elif not "low" in request.POST:
            form = TournamentRegistrationForm(request.POST)
            low_form = LowInTournamentForm()

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

                    message1 = (
                        "Inscripción en torneo",
                        f"Enhorabuena {cd['name']} te has registrado en el torneo {torneo.title}",
                        "info@ajedrezmalaga.org",
                        [f"{cd['mail']}"],
                    )
                    message2 = (
                        "Inscripción en torneo",
                        f"{cd['name']} {cd['surnames']} se ha registrado en el torneo {torneo.title}",
                        "info@ajedrezmalaga.org",
                        ["admin@ajedrezmalaga.org"],
                    )

                    send_mass_mail((message1, message2), fail_silently=False)

                    submitted_form = True
                    form = TournamentRegistrationForm()  # borrar campos crear form nuevo

    # else:
    #     form = TournamentRegistrationForm()
    #     low_form = LowInTournamentForm()

    return render(
        request,
        "core/torneo-detail.html",
        {
            "torneo": torneo,
            "allow_registration": allow_registration,
            "recaptcha_site_key": settings.GOOGLE_RECAPTCHA_SITE_KEY,
            "form": form,
            "submitted_form": submitted_form,
            "low_form": low_form,
        },
    )


def historico_torneos(request, year=None, month=None, all_tournaments=None):
    '''Vamos a obtener los torneos de los dos años anteriores al año en curso, los
    torneos del año en curso y los torneos de un año y un mes'''

    year_month_tournaments = None
    get_all_tournaments = False
    qs = False
    formatted_date = ''
    before_last_year = str(int(timezone.now().strftime("%Y")) - 2)
    last_year = str(int(timezone.now().strftime("%Y")) - 1)
    current_year = timezone.now().strftime("%Y")
    # current_month = timezone.now().strftime("%m")

    if all_tournaments:
        get_all_tournaments = Torneo.objects.all()

    if year and month:
        year_month_tournaments = Torneo.objects.filter(
            start__year=int(year), start__month=int(month)
        )
        qs = True
        formatted_date = datetime.datetime(year, month, 17).strftime("%B %Y")
        print(formatted_date)

    # todos los torneos cuya fecha de comienzo es el mes actual del año curso
    # current_month_tournaments = Torneo.objects.filter(start__month=current_month)
    current_year_tournaments = Torneo.objects.filter(start__year=current_year)

    return render(
        request,
        "core/historico-torneos.html",
        {
            "current_year_tournaments": current_year_tournaments,
            'current_year': current_year,
            'last_year': last_year,
            'before_last_year': before_last_year,
            'year_month_tournaments': year_month_tournaments,
            'qs': qs,
            'formatted_date': formatted_date,
            'get_all_tournaments': get_all_tournaments
        },
    )


# def todo_historico(request):
#     all_tournaments = Torneo.objects.all()

#     return render(
#         request, 'core/historico-torneos.html', {'all_tournaments': all_tournaments}
#     )
