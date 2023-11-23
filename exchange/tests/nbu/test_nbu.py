import json
from pathlib import Path
from unittest.mock import MagicMock

import responses

from exchange.currency_provider import NBUProvider, SellBuy


def get_json():
    current_directory = Path(__file__).parent
    with open(current_directory / 'rates.json', 'r') as file:
        data = json.load(file)
    return data


def test_nbu_currency_provider():
    provider = NBUProvider("USD", "UAH")
    rate_mocked = MagicMock(return_value=SellBuy(sell=27.0, buy=27.0))
    provider.get_rate = rate_mocked
    rate = provider.get_rate()
    assert rate == SellBuy(sell=27.0, buy=27.0)
    rate_mocked.assert_called()


@responses.activate
def test_nbu_with_data():
    responses.get(
        "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json",
        json=get_json(),
    )

    provider = NBUProvider("USD", "UAH")
    rate = provider.update()
    assert rate == SellBuy(sell=36.0675, buy=36.0675)

    provider = NBUProvider("EUR", "UAH")
    rate = provider.update()
    assert rate == SellBuy(sell=39.3352, buy=39.3352)
