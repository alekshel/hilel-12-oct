import json
from pathlib import Path
from unittest.mock import MagicMock

import responses

from exchange.currency_provider import VkurseProvider, SellBuy


def get_json():
    current_directory = Path(__file__).parent
    with open(current_directory / "rates.json", "r") as file:
        data = json.load(file)
    return data


def test_vkurse_currency_provider():
    provider = VkurseProvider("USD", "UAH")
    rate_mocked = MagicMock(return_value=SellBuy(sell=27.0, buy=27.0))
    provider.get_rate = rate_mocked
    rate = provider.get_rate()
    assert rate == SellBuy(sell=27.0, buy=27.0)
    rate_mocked.assert_called()


@responses.activate
def test_vkurse_with_data():
    responses.get(
        "https://vkurse.dp.ua/course.json",
        json=get_json(),
    )

    provider = VkurseProvider("USD", "UAH")
    rate = provider.update()
    assert rate == SellBuy(sell=39.55, buy=38.05)

    provider = VkurseProvider("EUR", "UAH")
    rate = provider.update()
    assert rate == SellBuy(sell=42.05, buy=41.05)
