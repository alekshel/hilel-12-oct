from django import forms

from .models import Rate


class RateForm(forms.ModelForm):
    currency_from = forms.ModelMultipleChoiceField(
        queryset=Rate.objects.values_list("currency_from", flat=True).distinct(),
        required=True,
        widget=forms.Select(),
    )

    currency_to = forms.ModelMultipleChoiceField(
        queryset=Rate.objects.values_list("currency_to", flat=True).distinct(),
        required=True,
        widget=forms.Select(),
    )

    class Meta:
        model = Rate
        fields = []
