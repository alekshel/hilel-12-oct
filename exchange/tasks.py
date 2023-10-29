import datetime

from celery import shared_task

from .currency_provider import PROVIDERS
from .models import Rate


@shared_task
def pull_rate():
    currencies = (
        "EUR",
        "USD",
    )

    date = datetime.date.today()
    for provider_class in PROVIDERS:
        for currency_name in currencies:
            provider = provider_class(currency_name, "UAH")
            print(currency_name, provider.name)

            current_currency = Rate.objects.filter(
                currency_from=currency_name,
                currency_to="UAH",
                provider=provider.name,
                date=date,
            )

            if not current_currency.exists():
                print(
                    f"Record for {currency_name} and {provider.name} not found, creating."
                )
                current_currency_rate = provider.update()
                created_currency = Rate.objects.create(
                    currency_from=currency_name,
                    currency_to="UAH",
                    sell=current_currency_rate.sell,
                    buy=current_currency_rate.buy,
                    provider=provider.name,
                    date=date,
                )
                print(
                    f"Created {currency_name} exchange rate with ID",
                    created_currency.id,
                )
