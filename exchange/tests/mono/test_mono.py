import json
from pathlib import Path
from unittest.mock import MagicMock

import responses

from exchange.currency_provider import MonoProvider, SellBuy


def get_json():
    current_directory = Path(__file__).parent
    with open(current_directory / "rates.json", "r") as file:
        data = json.load(file)
    return data


def test_mono_currency_provider():
    provider = MonoProvider("USD", "UAH")
    rate_mocked = MagicMock(return_value=SellBuy(sell=27.0, buy=27.0))
    provider.get_rate = rate_mocked
    rate = provider.get_rate()
    assert rate == SellBuy(sell=27.0, buy=27.0)
    rate_mocked.assert_called()


@responses.activate
def test_mono_with_data():
    responses.get(
        "https://api.monobank.ua/bank/currency",
        json=get_json(),
    )

    provider = MonoProvider("USD", "UAH")
    rate = provider.update()
    assert rate == SellBuy(sell=37.2995, buy=36.07)

    provider = MonoProvider("EUR", "UAH")
    rate = provider.update()
    assert rate == SellBuy(sell=40.7498, buy=39.31)
