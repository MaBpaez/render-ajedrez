from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "type": "search",
                "placeholder": "Buscar...",
                "aria-label": "Search",
                "class": "form-control me-2",
            }
        ),
    )
