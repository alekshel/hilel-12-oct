import json
from pathlib import Path
from unittest.mock import MagicMock

import responses

from exchange.currency_provider import PrivatbankProvider, SellBuy


def get_json():
    current_directory = Path(__file__).parent
    with open(current_directory / "rates.json", "r") as file:
        data = json.load(file)
    return data


def test_pb_currency_provider():
    provider = PrivatbankProvider("USD", "UAH")
    rate_mocked = MagicMock(return_value=SellBuy(sell=27.0, buy=27.0))
    provider.get_rate = rate_mocked
    rate = provider.get_rate()
    assert rate == SellBuy(sell=27.0, buy=27.0)
    rate_mocked.assert_called()


@responses.activate
def test_pb_with_data():
    responses.get(
        "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5",
        json=get_json(),
    )

    provider = PrivatbankProvider("USD", "UAH")
    rate = provider.update()
    assert rate == SellBuy(sell=37.55, buy=37.05)

    provider = PrivatbankProvider("EUR", "UAH")
    rate = provider.update()
    assert rate == SellBuy(sell=41.05, buy=40.05)
