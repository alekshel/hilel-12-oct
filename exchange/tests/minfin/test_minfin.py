import json
from pathlib import Path
from unittest.mock import MagicMock

import responses

from exchange.currency_provider import MinfinInterbankProvider, SellBuy


def get_json():
    current_directory = Path(__file__).parent
    with open(current_directory / 'rates.json', 'r') as file:
        data = json.load(file)
    return data


def test_minfin_currency_provider():
    provider = MinfinInterbankProvider("USD", "UAH")
    rate_mocked = MagicMock(return_value=SellBuy(sell=27.0, buy=27.0))
    provider.get_rate = rate_mocked
    rate = provider.get_rate()
    assert rate == SellBuy(sell=27.0, buy=27.0)
    rate_mocked.assert_called()


@responses.activate
def test_minfin_with_data():
    responses.get(
        "https://minfin.com.ua/api/currency/simple/?base=UAH&list=usd,eur",
        json=get_json(),
    )

    provider = MinfinInterbankProvider("USD", "UAH")
    rate = provider.update()
    assert rate == SellBuy(sell=36.075, buy=36.055)

    provider = MinfinInterbankProvider("EUR", "UAH")
    rate = provider.update()
    assert rate == SellBuy(sell=39.2243, buy=39.2062)
