import requests
import json
from config import keys,headers
class ConvertExcept(Exception):
    pass
class CurrencyConvector:
    @staticmethod
    def convert(values):
        values = values
        quote, base, amount = values
        base_ticet=keys.get(base)
        quote_ticet=keys.get(quote)
        if len(values) > 3:
            raise ConvertExcept("Слишком много параметров")

        if len(values) < 3:
            raise ConvertExcept("Недостаточно параметров")

        if quote == base:
            raise ConvertExcept(f"Невозможно перевести одинаковые валюты {base}.")

        if float(amount) < 0:
            raise ConvertExcept("Вы не можете конвертировать отрицательное количество валюты")

        if base_ticet not in keys.values():
            raise ConvertExcept(f"Выбрана неподдерживаемая валюта {base}")

        if quote_ticet not in keys.values():
            raise ConvertExcept(f"Выбрана неподдерживаемая валюта {quote}")

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertExcept(f"Не удалось обработать количество {amount}")

        url = f"https://api.apilayer.com/currency_data/convert?to={base_ticet}&from={quote_ticet}&amount={amount}"

        response = requests.request("GET", url, headers=headers)
        status_code = response.status_code
        result = response.text
        total_base= json.loads(result)
        return total_base