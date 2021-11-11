import os
import time
import gspread  # pip install gspread
import telebot  # pip install pyTelegramBotAPI
import requests
from dotenv import load_dotenv  # pip install python-dotenv
from os.path import join, dirname

"""Keys from .env"""


def get_from_env(key):
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)


"""This part about gdrive table"""


def google_tab(key):
    gc = gspread.service_account(filename='service_account.json')
    sh = gc.open_by_key(key)
    worksheet = sh.sheet1
    values_list = worksheet.col_values(3)  # list with all hb day
    bd_list = []  # birthday people list
    current_time = time.strftime("%d.%m")
    for i in range(1, len(values_list)):
        bd_date = values_list[i]
        bd_date_chk = bd_date[0:2] + '.' + bd_date[3:5]
        if bd_date_chk == current_time:
            bd_list.append(worksheet.cell(i + 1, 2).value)
    return bd_list


"""Getting GIF from api.giphy.com"""


def my_gif(key):
    endpoint = "https://api.giphy.com/v1/gifs/random"
    params = {"api_key": key, "tag": "happy birthday", "rating": "g"}
    response = requests.get(endpoint, params=params).json()
    result = response['data']['images']['downsized_large']['url']
    return result




"""MAIN 
PROGRAMM"""


def lambda_handler(event, context):
    bot = telebot.TeleBot(get_from_env('TELEGRAM_API'))
    gif_api_key = get_from_env('GIF_API')
    google_token_key = get_from_env('GOOGLE_TOKEN')
    bd_names = google_tab(google_token_key)
    bd_names_print = ', '.join([i for i in bd_names])
    if len(bd_names) > 0:
        my_text = f"{bd_names_print}! Клуб Run4Fun.by от всей души поздравляет с днем рождения!"
        chat_id = 476199692
        bot.send_message(chat_id=chat_id, text=my_text)
        bot.send_animation(chat_id=chat_id, animation=my_gif(gif_api_key))
    else:
        chat_id = 476199692
        bot.send_message(chat_id=chat_id, text='Сегодня именинников нет')