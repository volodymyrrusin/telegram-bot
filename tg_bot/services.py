import requests
import sqlalchemy.exc

from .models import PhoneBook
from tg_bot import db
from pprint import pprint
import re


class WeatherServiceException(Exception):
    pass


class PhonebookServiceException(Exception):
    pass


class CurrencyServiceException(Exception):
    pass


class WeatherService:
    GEO_URL = 'https://geocoding-api.open-meteo.com/v1/search'
    WEATHER_URL = 'https://api.open-meteo.com/v1/forecast'

    @staticmethod
    def get_geo_data(city_name):
        params = {
            'name': city_name
        }
        res = requests.get(f'{WeatherService.GEO_URL}', params=params)
        if res.status_code != 200:
            raise WeatherServiceException('Cannot get geo data')
        elif not res.json().get('results'):
            raise WeatherServiceException('City not found')
        return res.json().get('results')

    @staticmethod
    def get_current_weather_by_geo_data(lat, lon):
        params = {
            'latitude': lat,
            'longitude': lon,
            'current_weather': True
        }
        res = requests.get(f'{WeatherService.WEATHER_URL}', params=params)
        result = res.json().get('current_weather')
        if res.status_code != 200:
            raise WeatherServiceException('Cannot get geo data')
        return f"At {result.get('time')}:\n temperature is {result.get('temperature')}\n windspeed is {result.get('windspeed')}"


class PhonebookServices:

    @staticmethod
    def add_new_record(user_id, name, phone_number):
        if not re.fullmatch(r'^(\+380|380|0)\d{9}$', phone_number):
            raise PhonebookServiceException('Phone number has an incorrect format')
        record = PhoneBook(
            user_id=user_id,
            name=name,
            phone_number=phone_number
        )
        try:
            db.session.add(record)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            raise PhonebookServiceException('Phone number already exist')

    @staticmethod
    def delete_record(user_id, name):
        record = db.session.query(PhoneBook).filter_by(user_id=user_id, name=name).scalar()
        db.session.delete(record)
        db.session.commit()

    @staticmethod
    def list_of_contacts(user_id):
        contacts_list = db.session.execute(db.Select(PhoneBook).filter_by(user_id=user_id)).scalars()
        res = ''
        for contact in contacts_list:
            res += f'{contact.name} \n'
        return res

    @staticmethod
    def show_phone_number(user_id, name):
        phone_number = db.session.execute(
            db.Select(PhoneBook.phone_number).filter_by(user_id=user_id, name=name)).scalar()
        return phone_number


class CurrencyService:
    CURRENCY_URL = 'https://api.twelvedata.com/price?'
    API_KEY = 'fb016695c5484b369afbf449299c128b'

    @staticmethod
    def get_currency_rate(ticker):
        params = {
            'symbol': ticker,
            'apikey': CurrencyService.API_KEY
        }
        res = requests.get(f'{CurrencyService.CURRENCY_URL}', params=params)
        pprint(res.json())
        if res.status_code != 200:
            raise CurrencyServiceException('Cannot get currency data')
        return res.json().get('price')
