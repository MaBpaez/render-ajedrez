from django.core.mail import send_mass_mail
from celery import shared_task


@shared_task
def register_created(clean_data, torneo_title):
    """Tarea para enviar email cuando hay un registro en un torneo de la diputacion"""

    cd = clean_data

    message1 = (
        "Inscripción en torneo",
        f"Enhorabuena {cd['name']} te has registrado en el torneo {torneo_title}",
        "ajedrezmalaga@gmail.com",
        [f"{cd['mail']}"],
    )
    message2 = (
        "Inscripción en torneo",
        f"{cd['name']} {cd['surnames']} se ha registrado en el torneo {torneo_title}",
        "ajedrezmalaga@gmail.com",
        ["bravopaezm.15@gmail.com"],
    )

    """Esta parte es solo si utilizamos un decorador como hace celery con el
    decorador @task, es así por definición de como se usan los decoradores en python."""

    mail_sent = send_mass_mail((message1, message2), fail_silently=False)

    return mail_sent


@shared_task
def low_created(clean_data, torneo_title):
    """Tarea para enviar email cuando hay una baja en un torneo de la diputacion"""

    cd = clean_data

    message1 = (
        "Baja en torneo",
        f"Enhorabuena {cd['name']} te has dado de baja en el torneo {torneo_title}",
        "ajedrezmalaga@gmail.com",
        [f"{cd['mail']}"],
    )
    message2 = (
        "Baja en torneo",
        f"{cd['name']} {cd['surnames']} se ha dado de baja en el torneo {torneo_title}",
        "ajedrezmalaga@gmail.com",
        ["bravopaezm.15@gmail.com"],
    )

    """Esta parte es solo si utilizamos un decorador como hace celery con el
    decorador @task, es así por definición de como se usan los decoradores en python."""

    mail_sent = send_mass_mail((message1, message2), fail_silently=False)

    return mail_sent
