import dataclasses
from abc import ABC, abstractmethod

import requests


@dataclasses.dataclass
class SellBuy:
    sell: float
    buy: float


class RateNotFound(Exception):
    pass


class ProviderBase(ABC):
    name = None
    url = ""

    def __init__(self, currency_from: str, currency_to: str):
        self.currency_from = currency_from
        self.currency_to = currency_to

    def get_rate(self):
        response = requests.get(self.url)
        response.raise_for_status()
        return response.json()

    def update(self):
        for currency in self.get_rate():
            if self.condition(currency):
                return self.get_value(currency)
        raise RateNotFound(
            f"Cannot find rate from {self.currency_from} to {self.currency_to} in provider {self.name}"
        )

    @abstractmethod
    def condition(self, currency):
        pass

    @abstractmethod
    def get_value(self, currency) -> SellBuy:
        pass


class MonoProvider(ProviderBase):
    name = "monobank"
    url = "https://api.monobank.ua/bank/currency"

    iso_from_country_code = {
        "UAH": 980,
        "USD": 840,
        "EUR": 978,
    }

    def condition(self, currency):
        currency_from_code = self.iso_from_country_code[self.currency_from]
        currency_to_code = self.iso_from_country_code[self.currency_to]
        return (
            currency["currencyCodeA"] == currency_from_code
            and currency["currencyCodeB"] == currency_to_code
        )

    def get_value(self, currency) -> SellBuy:
        return SellBuy(sell=float(currency["rateSell"]), buy=float(currency["rateBuy"]))


class PrivatbankProvider(ProviderBase):
    name = "privatbank"
    url = "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5"

    def condition(self, currency):
        return (
            currency["ccy"] == self.currency_from
            and currency["base_ccy"] == self.currency_to
        )

    def get_value(self, currency) -> SellBuy:
        return SellBuy(buy=float(currency["buy"]), sell=float(currency["sale"]))


class NBUProvider(ProviderBase):
    name = "nbu"
    url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"

    def condition(self, currency):
        return currency["cc"] == self.currency_from

    def get_value(self, currency) -> SellBuy:
        return SellBuy(buy=float(currency["rate"]), sell=float(currency["rate"]))


class VkurseProvider(ProviderBase):
    name = "vkurse.dp.ua"
    url = "https://vkurse.dp.ua/course.json"

    def condition(self, currency):
        currency_name = ""
        if self.currency_from == "USD":
            currency_name = "Dollar"
        elif self.currency_from == "EUR":
            currency_name = "Euro"
        return currency[0] == currency_name

    def get_value(self, currency) -> SellBuy:
        return SellBuy(buy=float(currency[1]["buy"]), sell=float(currency[1]["sale"]))

    def update(self):
        for currency in self.get_rate().items():
            if self.condition(currency):
                return self.get_value(currency)
        raise RateNotFound(
            f"Cannot find rate from {self.currency_from} to {self.currency_to} in provider {self.name}"
        )


class MinfinInterbankProvider(ProviderBase):
    name = "minfin - interbank"
    url = "https://minfin.com.ua/api/currency/simple/?base=UAH&list=usd,eur"

    def condition(self, currency):
        return currency[0] == self.currency_from and currency[1]["interbank"]

    def get_value(self, currency) -> SellBuy:
        return SellBuy(
            buy=float(currency[1]["interbank"]["buy"]["val"]),
            sell=float(currency[1]["interbank"]["sell"]["val"]),
        )

    def update(self):
        for currency in self.get_rate()["data"].items():
            if self.condition(currency):
                return self.get_value(currency)
        raise RateNotFound(
            f"Cannot find rate from {self.currency_from} to {self.currency_to} in provider {self.name}"
        )


PROVIDERS = [
    MonoProvider,
    PrivatbankProvider,
    NBUProvider,
    VkurseProvider,
    MinfinInterbankProvider,
]
