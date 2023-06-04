import json

from tg_bot.handlers.callback_handler import TelegramHandler
from tg_bot.services.currency_service import *
from tg_bot.services.phonebook_service import *
from tg_bot.services.weather_service import *
from tg_bot.models import User
from tg_bot import db
from tg_bot.commands_list import commands_list


class MessageHandler(TelegramHandler):

    def __init__(self, data):
        self.user = User(**data.get('from'))
        self.text = data.get('text')
        if not db.session.scalar(db.Select(User).filter_by(id=self.user.id)):
            db.session.add(self.user)
            db.session.commit()

    def handle(self):
        match self.text.split():
            case['/commands']:
                self.send_message(commands_list)
            case '/price', symbol:
                try:
                    price = CurrencyService.get_current_price(symbol)
                except CurrencyServiceException as cse:
                    self.send_message(str(cse))
                else:
                    self.send_message(price)
            case '/convert', currency_pair, amount:
                try:
                    converted_amount = CurrencyService.convert_currency(currency_pair, amount)
                except CurrencyServiceException as cse:
                    self.send_message(str(cse))
                else:
                    self.send_message(converted_amount)
            case '/quote', symbol:
                try:
                    quote = CurrencyService.get_quote(symbol)
                except CurrencyServiceException as cse:
                    self.send_message(str(cse))
                else:
                    self.send_message(quote)
            case '/symbol', symbol:
                try:
                    symbols_data = CurrencyService.get_symbol(symbol)
                except CurrencyServiceException as cse:
                    self.send_message(str(cse))
                else:
                    buttons = []
                    for item in symbols_data:
                        instrument_button = {
                            'text': f'{item.get("symbol")} - {item.get("instrument_name")}',
                            'callback_data': json.dumps(
                                {'type': 'symbol', 'symbol': item.get('symbol')})
                        }
                        buttons.append([instrument_button])
                    markup = {
                        'inline_keyboard': buttons
                    }
                    self.send_markup_message('Choose an instrument from a list:', markup)
            case '/weather', city:
                try:
                    geo_data = WeatherService.get_geo_data(city)
                except WeatherServiceException as wse:
                    self.send_message(str(wse))
                else:
                    buttons = []
                    for item in geo_data:
                        city_button = {
                            'text': f'{item.get("name")} - {item.get("admin1")}',
                            'callback_data': json.dumps(
                                {'type': 'weather', 'lat': item.get('latitude'), 'lon': item.get('longitude')})
                        }
                        buttons.append([city_button])
                    markup = {
                        'inline_keyboard': buttons
                    }
                    self.send_markup_message('Choose a city from a list:', markup)
            case '/phonebook', 'add', name, phone_number:
                try:
                    PhonebookServices.add_record(self.user.id, name, phone_number)
                except PhonebookServiceException as pse:
                    self.send_message(str(pse))
                else:
                    self.send_message(f'{name} is added to a phonebook')
            case '/phonebook', 'delete', name:
                try:
                    PhonebookServices.delete_record(self.user.id, name)
                except PhonebookServiceException as pse:
                    self.send_message(str(pse))
                else:
                    self.send_message(f'{name} is deleted from a phonebook')
            case '/phonebook', 'show', name:
                try:
                    phone_number = PhonebookServices.show_phone_number(self.user.id, name)
                except PhonebookServiceException as pse:
                    self.send_message(str(pse))
                else:
                    self.send_message(phone_number)
            case '/phonebook', 'list':
                try:
                    contacts = PhonebookServices.list_of_contacts(self.user.id)
                except PhonebookServiceException as pse:
                    self.send_message(str(pse))
                else:
                    buttons = []
                    for item in contacts:
                        contact_button = {
                            'text': f'{item.name}',
                            'callback_data': json.dumps(
                                {'type': 'phonebook', 'user_id': self.user.id, 'name': item.name})
                        }
                        buttons.append([contact_button])
                    markup = {
                        'inline_keyboard': buttons
                    }
                    self.send_markup_message('Choose a contact from a list:', markup)
            case _:
                self.send_message('Command not recognized')
                self.send_message(commands_list)
