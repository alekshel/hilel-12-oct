from django.http import JsonResponse
from django.shortcuts import render

from .models import Rate
from .forms import RateForm


def main_view(request):
    response_data = {
        "current_rates": [
            {
                "id": rate.id,
                "date": rate.date,
                "vendor": rate.provider,
                "currency_a": rate.currency_from,
                "currency_b": rate.currency_to,
                "sell": rate.sell,
                "buy": rate.buy,
            }
            for rate in Rate.objects.all()
        ]
    }
    return JsonResponse(response_data)


def calc_view(request):
    sum_from = 100

    if not request.POST.get("currency_from"):
        current_from = (
            Rate.objects.values_list("currency_from", flat=True).distinct().first()
        )
    else:
        current_from = request.POST.get("currency_from")
    best_rate = Rate.objects.filter(currency_from=current_from).order_by("buy").first()

    if request.method == "POST":
        form = RateForm(request.POST)
    else:
        form = RateForm()

    rates = list()
    for rate in Rate.objects.filter(currency_from=current_from).all():
        rates.append(
            {
                "provider": rate.provider,
                "sum_to": float(rate.buy * sum_from),
            }
        )

    sum_rate = 0
    if best_rate:
        sum_rate = float(sum_from * best_rate.buy)

    return render(
        request,
        "calc_form.html",
        {
            "form": form,
            "current_from": current_from,
            "sum_from": sum_from,
            "sum_to": sum_rate,
            "rates": rates,
        },
    )
