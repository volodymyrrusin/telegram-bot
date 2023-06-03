import json
from tg_bot.services.currency_service import *
from tg_bot.services.phonebook_service import *
from tg_bot.services.weather_service import *
from tg_bot.models import User

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
            case 'symbol':
                try:
                    quote = CurrencyService.get_quote(**self.callback_data)
                except CurrencyServiceException as cse:
                    self.send_message(str(cse))
                else:
                    self.send_message(quote)
            case 'phonebook':
                try:
                    phone_number = PhonebookServices.show_phone_number(**self.callback_data)
                except PhonebookServiceException as pse:
                    self.send_message(str(pse))
                else:
                    self.send_message(phone_number)
