from django import forms

from .models import Rate


class RateForm(forms.Form):
    currency_from = forms.ChoiceField(
        choices=[("EUR", "EUR"), ("USD", "USD")],
        required=True,
        widget=forms.Select(),
    )

    currency_to = forms.ChoiceField(
        choices=[("UAH", "UAH")],
        required=True,
        widget=forms.Select(),
    )

    class Meta:
        model = Rate
        fields = []
