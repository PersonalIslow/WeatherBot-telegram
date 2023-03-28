import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()  # загрузить переменные среды из файла .env

# получить токен бота из переменных среды
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# URL для отправки запросов к Telegram API
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/'

# URL для отправки запросов к API погоды
WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'

# получить API ключ для OpenWeatherMap из переменных среды
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

# функция для отправки сообщений в Telegram
def send_message(chat_id, text):
    url = TELEGRAM_API_URL + 'sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, json=payload)
    return response.json()

# функция для получения информации о погоде в заданном городе
def get_weather(city):
    url = WEATHER_API_URL
    params = {'q': city, 'appid': WEATHER_API_KEY, 'units': 'metric'}
    response = requests.get(url, params=params)
    weather_data = json.loads(response.text)
    return weather_data

# функция для обработки запросов от пользователей
def handle_message(message):
    chat_id = message['chat']['id']
    text = message['text']
    if text.startswith('/weather'):
        city = text.split('/weather ')[-1]
        weather_data = get_weather(city)
        weather_description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        send_message(chat_id, f'The weather in {city} is {weather_description}, temperature is {temperature}°C')
    else:
        send_message(chat_id, 'Invalid command. Please type /weather CITY_NAME')

# функция для получения обновлений от Telegram API
def get_updates():
    url = TELEGRAM_API_URL + 'getUpdates'
    response = requests.get(url)
    updates = json.loads(response.text)['result']
    return updates

# функция для запуска бота
def run_bot():
    last_update_id = None
    while True:
        updates = get_updates()
        if updates:
            last_update = updates[-1]
            if last_update['update_id'] != last_update_id:
                handle_message(last_update['message'])
                last_update_id = last_update['update_id']

if __name__ == '__main__':
    run_bot()