import json
from flask import request

from .services import *
from .models import User
from tg_bot import db

BOT_TOKEN = os.getenv('BOT_TOKEN')
TG_BASE_URL = 'https://api.telegram.org/bot'


class TelegramHandler:
    user = None

    def send_markup_message(self, text, markup):
        data = {
            'chat_id': self.user.id,
            'text': text,
            'reply_markup': markup
        }
        requests.post(f'{TG_BASE_URL}{BOT_TOKEN}/sendMessage', json=data)

    def send_message(self, text):
        data = {
            'chat_id': self.user.id,
            'text': text
        }
        requests.post(f'{TG_BASE_URL}{BOT_TOKEN}/sendMessage', json=data)


class MessageHandler(TelegramHandler):

    def __init__(self, data):
        pprint(request.json)
        self.user = User(**data.get('from'))
        self.text = data.get('text')
        if db.session.query(User).filter_by(id=self.user.id).scalar() is None:
            db.session.add(self.user)
            db.session.commit()

    def handle(self):
        match self.text.split():
            case 'weather', city:
                try:
                    geo_data = WeatherService.get_geo_data(city)
                except WeatherServiceException as wse:
                    self.send_message(str(wse))
                else:
                    buttons = []
                    for item in geo_data:
                        test_button = {
                            'text': f'{item.get("name")} - {item.get("admin1")}',
                            'callback_data': json.dumps(
                                {'type': 'weather', 'lat': item.get('latitude'), 'lon': item.get('longitude')})
                        }
                        buttons.append([test_button])
                    markup = {
                        'inline_keyboard': buttons
                    }
                    self.send_markup_message('Choose a city from a list:', markup)
            case 'phonebook', 'add', name, phone_number:
                try:
                    PhonebookServices.add_new_record(self.user.id, name, phone_number)
                except PhonebookServiceException as pse:
                    self.send_message(str(pse))
                else:
                    self.send_message(f'{name} is added to a phonebook')
            case 'phonebook', 'delete', name:
                try:
                    PhonebookServices.delete_record(self.user.id, name)
                except Exception as e:
                    self.send_message(str(e))
                else:
                    self.send_message(f'{name} is deleted from a phonebook')
            case '/phonebook' 'list':
                try:
                    contacts = PhonebookServices.list_of_contacts(self.user.id)
                except Exception as e:
                    self.send_message(str(e))
                else:
                    self.send_message(contacts)
            case 'phonebook', 'show', name:
                try:
                    phone_number = PhonebookServices.show_phone_number(self.user.id, name)
                except Exception as e:
                    self.send_message(str(e))
                else:
                    self.send_message(phone_number)
            case 'currency' | 'stocks', ticker:
                try:
                    exchange_rate = CurrencyService.get_currency_rate(ticker)
                except Exception as e:
                    self.send_message(str(e))
                else:
                    self.send_message(exchange_rate)
            case ['/commands']:
                self.send_message('List of commands:\n'
                                  'weather <city> - show the weather for the city\n'
                                  'phonebook add <name> <phone_number> - add contact to the phonebook\n'
                                  'phonebook delete <name> - delete contact from the phonebook\n'
                                  'phonebook show <name> - show phone number of the contact\n'
                                  'phonebook list - show all the contacts')
            case _:
                self.send_message('Command not recognized')


class CallbackHandler(TelegramHandler):

    def __init__(self, data):
        self.user = User(**data.get('from'))
        self.callback_data = json.loads(data.get('data'))

    def handle(self):
        callback_type = self.callback_data.pop('type')
        match callback_type:
            case 'weather':
                try:
                    weather = WeatherService.get_current_weather_by_geo_data(**self.callback_data)
                except WeatherServiceException as wse:
                    self.send_message(str(wse))
                else:
                    self.send_message(weather)
