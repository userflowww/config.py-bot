
import requests
import json


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            raise APIException("Нельзя конвертировать валюту в саму себя.")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException("Некорректное количество валюты.")

        response = requests.get(f'https://api.exchangerate-api.com/v4/latest/{base}')
        data = json.loads(response.text)

        if 'rates' not in data or quote not in data['rates']:
            raise APIException("Неверная валюта или курс недоступен.")

        rate = data['rates'][quote]
        result = amount * rate
        return result