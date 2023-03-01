from django import forms


class ContactForm(forms.Form):
    AJEDREZ_CHOICES = (
        ("D", "Delegado"),
        ("S", "Secretario"),
        ("A", "Delegado y Secretario"),
    )

    nombre = forms.CharField(max_length=100)
    email = forms.EmailField()
    opcion = forms.ChoiceField(
        choices=AJEDREZ_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
    )
    mensaje = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": "6"})
    )
    politica_privacidad = forms.BooleanField()

    nombre.widget.attrs.update({"class": "form-control", "placeholder": "nombre"})
    email.widget.attrs.update({"class": "form-control", "placeholder": "@correo"})
