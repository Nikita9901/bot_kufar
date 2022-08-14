#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import telebot
from aiogram import Bot, types, Dispatcher, executor
import requests
import json

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}
# API_URL = "https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6MX0%3D&lang=ru&ot=1&prn=17000&query=iphone&size=42"
# API_URL = "https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6MX0%3D&lang=ru&prn=17000&size=42"
TOKEN = "5536067676:AAHjPs_FfXfeVFL1rhxej8sppmfu-f2uhCQ"


def get_page(url):
    s = requests.Session()
    response = s.get(url=url, headers=headers)

    with open("index.html", "w") as file:
        file.write(response.text)


# def get_data():
#     global start_info
#     s = requests.Session()
#     response = s.get(url=API_URL, headers=headers)
#     data = response.json()
#     for i in range(10):
#         if data.get("ads")[9-i].get("ad_parameters")[0].get("vl") == "Мобильные телефоны":
#             print(f'{data.get("ads")[9-i].get("subject")}: {int(data.get("ads")[9-i].get("price_byn"))/100}')
#             start_info.append({
#                 "ad_id": data.get("ads")[9-i].get("ad_id"),
#                 "subject": data.get("ads")[9-i].get("subject"),
#                 "price": int(data.get("ads")[9-i].get("price_byn"))/100,
#                 "ad_link": data.get("ads")[9-i].get("ad_link")
#             })
#             ad_ids.append(data.get("ads")[9-i].get("ad_id"))


# def update_data():
#     global start_info
#     global update_info
#     s = requests.Session()
#     response = s.get(url=API_URL, headers=headers)
#     data = response.json()
#     update_info = []
#     for i in range(10):
#         if data.get("ads")[9-i].get("ad_parameters")[0].get("vl") == "Мобильные телефоны":
#             update_info.append({
#                 "ad_id": data.get("ads")[9-i].get("ad_id"),
#                 "subject": data.get("ads")[9-i].get("subject"),
#                 "price": int(data.get("ads")[9-i].get("price_byn"))/100
#             })
#     for ad in update_info:
#         if ad.get("ad_id") not in ad_ids:
#             print(ad.get("subject"))
#             print(ad.get("price"))
#             ad_ids.append(ad.get("ad_id"))
#     start_info = update_info



def get_json(url):
    s = requests.Session()
    response = s.get(url=url, headers=headers)

    with open("result.json", "w") as file:
        json.dump(response.json(), file, indent=4, ensure_ascii=False)


def main():
    # get_page(url="https://www.kufar.by/l/telefony-i-planshety?ot=1&query=iphone&rgn=all")
    # get_json(url=API_URL)
    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot)

    @dp.message_handler(commands=['start'])
    async def get_text_messages(message: types.Message):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Iphone", "All"]
        keyboard.add(*buttons)
        await message.answer("Какие телефоны искать?", reply_markup=keyboard)

    @dp.message_handler(lambda message: message.text == "Iphone")
    async def searchIphone(message: types.Message):
        ad_ids = []
        API_URL="https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6MX0%3D&lang=ru&ot=1&query=iphone&size=42"
        await message.reply("Начинаю поиск Iphone", reply_markup=types.ReplyKeyboardRemove())
        # await bot.send_message(message.from_user.id, "Iphone или Все?", parse_mode="Markdown")
        # if message.text == "Все":
        #     print("Все")
        while (True):
            s = requests.Session()
            try:
                response = s.get(url=API_URL, headers=headers)
                data = response.json()
                update_info = []
                for i in range(10):
                    if data.get("ads")[9 - i].get("ad_parameters")[0].get("vl") == "Мобильные телефоны":
                        update_info.append({
                            "ad_id": data.get("ads")[9 - i].get("ad_id"),
                            "subject": data.get("ads")[9 - i].get("subject"),
                            "price": int(data.get("ads")[9 - i].get("price_byn")) / 100,
                            "ad_link": data.get("ads")[9 - i].get("ad_link")

                        })
                for ad in update_info:
                    if ad.get("ad_id") not in ad_ids:
                        print(f'{ad.get("subject")}: {ad.get("price")}')
                        await bot.send_message(message.from_user.id, f"""
                [{ad.get('subject')}]({ad.get('ad_link')}) : {ad.get('price')} BYN.

                """, parse_mode="Markdown")
                        ad_ids.append(ad.get("ad_id"))
                time.sleep(5)
            except:
                await bot.send_message(message.from_user.id, "Ошибка сервера", parse_mode="Markdown")
                print("Ошибка сервера")
                time.sleep(5)
                continue
        await bot.send_message(message.from_user.id, "Пока!", parse_mode="Markdown")

    @dp.message_handler(lambda message: message.text == "All")
    async def searchAll(message: types.Message):
        ad_ids = []
        API_URL = "https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=17010&cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6MX0%3D&lang=ru&size=42"
        await message.reply("Начинаю поиск всех телефонов", reply_markup=types.ReplyKeyboardRemove())
        # await bot.send_message(message.from_user.id, "Iphone или Все?", parse_mode="Markdown")
        # if message.text == "Все":
        #     print("Все")
        while (True):
            s = requests.Session()
            try:
                response = s.get(url=API_URL, headers=headers)
                data = response.json()
                update_info = []
                for i in range(10):
                    if data.get("ads")[9 - i].get("ad_parameters")[0].get("vl") == "Мобильные телефоны":
                        update_info.append({
                            "ad_id": data.get("ads")[9 - i].get("ad_id"),
                            "subject": data.get("ads")[9 - i].get("subject"),
                            "price": int(data.get("ads")[9 - i].get("price_byn")) / 100,
                            "ad_link": data.get("ads")[9 - i].get("ad_link")

                        })
                for ad in update_info:
                    if ad.get("ad_id") not in ad_ids:
                        print(f'{ad.get("subject")}: {ad.get("price")}')
                        await bot.send_message(message.from_user.id, f"""
                    [{ad.get('subject')}]({ad.get('ad_link')}) : {ad.get('price')} BYN.

                    """, parse_mode="Markdown")
                        ad_ids.append(ad.get("ad_id"))
                time.sleep(5)
            except:
                await bot.send_message(message.from_user.id, "Ошибка сервера", parse_mode="Markdown")
                print("Ошибка сервера")
                time.sleep(5)
                continue
        await bot.send_message(message.from_user.id, "Пока!", parse_mode="Markdown")

    executor.start_polling(dp)

if __name__ == '__main__':
    main()