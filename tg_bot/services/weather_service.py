import requests


class WeatherServiceException(Exception):
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
        return f"As of {result.get('time')}:\n " \
               f"Temperature: {result.get('temperature')}\n " \
               f"Windspeed: {result.get('windspeed')}"
