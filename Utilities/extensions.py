import requests
import json
from base_data import cur_list, API_KEY


class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def errors_check(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f"Невозможно конвертировать одинаковые валюты в {base}.")

        try:
            quote_ticker = cur_list[quote]
        except KeyError:
            raise ConvertionException(f"Неправильно введена валюта {quote}.")

        try:
            base_ticker = cur_list[base]
        except KeyError:
            raise ConvertionException(f"Неправильно введена валюта {base}.")

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f"Неправильно введено количество {base}.")

        r = requests.get(f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{base_ticker}/{quote_ticker}/{amount}")
        total_base = json.loads(r.content)['conversion_result']
        message = f'Цена {amount} {quote_ticker} в {base_ticker} : {total_base}'


        return message


