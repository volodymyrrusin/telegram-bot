import requests
import os


class CurrencyServiceException(Exception):
    pass


class CurrencyService:
    CURRENCY_URL = 'https://api.twelvedata.com'
    CURRENCY_API_KEY = os.getenv('CURRENCY_API_KEY')

    @staticmethod
    def get_current_price(symbol):
        http_route = '/price'
        params = {
            'symbol': symbol,
            'apikey': CurrencyService.CURRENCY_API_KEY,
            'dp': '2'
        }
        res = requests.get(f'{CurrencyService.CURRENCY_URL}{http_route}?', params=params)
        if res.status_code != 200:
            raise CurrencyServiceException('Cannot get price data')
        elif not res.json().get('price'):
            raise CurrencyServiceException('Currency not found')
        return res.json().get('price')

    @staticmethod
    def convert_currency(symbol, amount):
        http_route = '/currency_conversion'
        params = {
            'symbol': symbol,
            'amount': amount,
            'apikey': CurrencyService.CURRENCY_API_KEY,
            'dp': '2'
        }
        res = requests.get(f'{CurrencyService.CURRENCY_URL}{http_route}?', params=params)
        if res.status_code != 200:
            raise CurrencyServiceException('Cannot get conversion data')
        elif not res.json().get('amount'):
            raise CurrencyServiceException('Currency pair not found')
        return f"Rate: {res.json().get('rate')}\n" \
               f"Amount: {res.json().get('amount')}"

    @staticmethod
    def get_quote(symbol):
        http_route = '/quote'
        params = {
            'symbol': symbol,
            'apikey': CurrencyService.CURRENCY_API_KEY,
            'dp': '2'
        }
        res = requests.get(f'{CurrencyService.CURRENCY_URL}{http_route}?', params=params)
        if res.status_code != 200:
            raise CurrencyServiceException('Cannot get instrument data')
        elif not res.json().get('name'):
            raise CurrencyServiceException('Instrument not found')
        response = f"Name: {res.json().get('name')}\n" \
                   f"Exchange: {res.json().get('exchange')}\n" \
                   f"Currency: {res.json().get('currency')}\n" \
                   f"52 week low: {res.json().get('fifty_two_week').get('low')}\n" \
                   f"52 week high: {res.json().get('fifty_two_week').get('high')}"
        return response

    @staticmethod
    def get_symbol(symbol):
        http_route = '/symbol_search'
        params = {
            'symbol': symbol,
            'apikey': CurrencyService.CURRENCY_API_KEY,
            'outputsize': '10'
        }
        res = requests.get(f'{CurrencyService.CURRENCY_URL}{http_route}?', params=params)
        if res.status_code != 200:
            raise CurrencyServiceException('Cannot get instruments data')
        elif not res.json().get('data'):
            raise CurrencyServiceException('Instruments data not found')
        return res.json().get('data')
