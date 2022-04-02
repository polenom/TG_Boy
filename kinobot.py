import random
import time
import requests, json
from sdate import *
import telebot
from telebot import types
from bs4 import BeautifulSoup
import datetime
bot = telebot.TeleBot(TOKEN)
params = dict(q='Minsk',appid=APIKEY_OPENW,units='metric')



@bot.message_handler(commands=['weather'])
def weather(message):
    x = requests.get(f'https://api.openweathermap.org/data/2.5/weather', params=params)
    we = x.json()
    bot.send_message(message.chat.id, f'In Minsk temp {we["main"]["temp"]} feel {we["main"]["feels_like"]} and speed wind {we["wind"]["speed"]}')


@bot.message_handler(commands=['kino'])
def show_kino(message):
    afisha = requests.get('https://afisha.me/today/film/')
    soup = BeautifulSoup(afisha.text, 'html.parser', multi_valued_attributes=None)
    for i in soup.find(id='events-block').findAll('ul')[:2]:
        for i1 in i.findAll('li'):

            keyboard = types.InlineKeyboardMarkup()
            url_But = types.InlineKeyboardButton(text='купить билеты', url=i1.a['href'])
            keyboard.add(url_But)
            bot.send_photo(message.chat.id, i1.img['src'])
            bot.send_message(message.chat.id, f'{i1.img["alt"]} \n {i1.div.p.text}', reply_markup=keyboard)

print(datetime.date.today().day)

@bot.message_handler(commands=['covid'])
def show_covid(message):
    date = datetime.date.today()
    url = 'https://api.covid19api.com/total/country/Belarus'
    params={'to':f'{date.year}-{date.month}-{date.day}T00:00:00Z', 'from':f'{date.year}-{date.month}-{date.day-1}T00:00:00Z'}
    covid = requests.get(url,params=params)
    covidreturn = covid.json()[0]
    bot.send_message(message.chat.id, text=f'In belarus have  confim {covidreturn["Confirmed"]} deaths {covidreturn["Deaths"]} active {covidreturn["Active"]} at {date}')


@bot.message_handler(commands=['quoti'])
def show_quoti(message):
    url_break_bead = "https://www.breakingbadapi.com/api/quotes"
    date = requests.get(url_break_bead)
    date_json= date.json()
    randomm =random.randrange(0,len(date_json)-1)
    bot.send_message(message.chat.id, text=f'{date_json[randomm]["quote"]}\n Author: {date_json[randomm]["author"]}')


@bot.message_handler(commands=['joke'])
def show_joke(message):
    joke=requests.get('https://api.chucknorris.io/jokes/random').json()
    bot.send_message(message.chat.id, text=f'{joke["value"]}')

@bot.message_handler(content_types=['text'])
def any_msg(message):
    print(message.text)
    if message.text == 'go':
        markup = types.ReplyKeyboardMarkup(row_width=2,one_time_keyboard=True,resize_keyboard=True)
        itembtn1 = types.KeyboardButton('/kino')
        itembtn2 = types.KeyboardButton('/weather')
        itembtn3 = types.KeyboardButton('/covid')
        itembtn4 = types.KeyboardButton('/quoti')
        itembtn5 = types.KeyboardButton('/joke')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)
        bot.send_message(message.chat.id, "List full commands :", reply_markup=markup)

# def any_msg(message):
#     keyboard = types.InlineKeyboardMarkup()
#     switch_button = types.InlineKeyboardButton(text="Нажми меня", switch_inline_query="Telegram")
#     keyboard.add(switch_button)
#     bot.send_message(message.chat.id, "Я – сообщение из обычного режима", reply_markup=keyboard)
#     time.sleep(2)

if __name__=="__main__":
    bot.infinity_polling()