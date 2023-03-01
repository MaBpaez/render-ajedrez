from django import forms
from .models import TournamentRegistration


class TournamentRegistrationForm(forms.ModelForm):
    class Meta:
        model = TournamentRegistration
        fields = [
            "name",
            "surnames",
            "mail",
            "population",
            "zip_code",
            "date_birth",
            "phone",
            "privacy_policy",
            "tournament_title",
            "status",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "surnames": forms.TextInput(attrs={"class": "form-control"}),
            "population": forms.TextInput(attrs={"class": "form-control"}),
            "zip_code": forms.TextInput(attrs={"class": "form-control"}),
            "mail": forms.EmailInput(attrs={"class": "form-control"}),
            "privacy_policy": forms.CheckboxInput(
                attrs={"class": "form-check-label", "required": True}
            ),
            "phone": forms.TextInput(
                attrs={
                    "type": "tel",
                    "required": True,
                    "pattern": "[0-9]{3}[0-9]{3}[0-9]{3}",
                    "placeholder": "666555333",
                    "class": "form-control",
                }
            ),
            "date_birth": forms.TextInput(
                attrs={
                    "type": "date",
                    "required": True,
                    "class": "form-control",
                }
            ),
        }


class LowInTournamentForm(forms.Form):
    name = forms.CharField(max_length=100)
    surnames = forms.CharField(max_length=150)
    mail = forms.EmailField()
    privacy_policy = forms.BooleanField()

    name.widget.attrs.update({"class": "form-control"})
    surnames.widget.attrs.update({"class": "form-control"})
    mail.widget.attrs.update({"class": "form-control"})
    privacy_policy.widget.attrs.update({"class": "form-check-label", "required": True})
