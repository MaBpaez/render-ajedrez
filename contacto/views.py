import requests
from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm


def contact(request):

    if request.method == "POST":
        form = ContactForm(request.POST)
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
                print("FORMULARIO ENVIADO CON ÉXITO")
                # diccionario datos limpios
                cd = form.cleaned_data
                # Enviamos los datos
                if cd['opcion'] == 'D':
                    send_mail(
                        f"Nombre: {cd['nombre']}",
                        f"Correo electrónico: {cd['email']}\nPolítica Privacidad: {cd['politica_privacidad']}\n"
                        f"Mensaje:\n\n{cd['mensaje']}",
                        "ajedrezmalaga@gmail.com",
                        ["bravopaezm.15@gmail.com"],
                    )
                elif cd['opcion'] == 'S':
                    send_mail(
                        f"Nombre: {cd['nombre']}",
                        f"Correo electrónico: {cd['email']}\nPolítica Privacidad: {cd['politica_privacidad']}\n"
                        f"Mensaje:\n\n{cd['mensaje']}",
                        "ajedrezmalaga@gmail.com",
                        ["py.v3.6.3@gmail.com"],
                    )
                elif cd['opcion'] == 'A':
                    send_mail(
                        f"Nombre: {cd['nombre']}",
                        f"Correo electrónico: {cd['email']}\nPolítica Privacidad: {cd['politica_privacidad']}\n"
                        f"Mensaje:\n\n{cd['mensaje']}",
                        "ajedrezmalaga@gmail.com",
                        ["bravopaezm.15@gmail.com", "py.v3.6.3@gmail.com"],
                    )

                # Redireccionamos
                messages.success(
                    request,
                    "Gracias por contactar, en breve nos pondremos en contacto contigo.",
                    extra_tags="success",
                )
            else:
                messages.error(
                    request,
                    "ReCAPTCHA no válido. Inténtalo de nuevo.",
                    extra_tags="error",
                )

    else:
        form = ContactForm()

    return render(
        request,
        "contacto/contact.html",
        {"form": form, "recaptcha_site_key": settings.GOOGLE_RECAPTCHA_SITE_KEY},
    )
