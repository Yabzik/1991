import telebot
from telebot import types
import time
import datetime
import urllib.request, json 

bot = telebot.TeleBot("1047628795:AAHR8i8R8Nri4nVmcAyOZTackPe3jvnPk3c")
path = ''
course = ''
time = ''
notif = ''

@bot.message_handler(commands=['subject'])
def handle_text(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Получить расписание')
    user_markup.row('Уведомления')
    bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=user_markup)
    
@bot.message_handler(func=lambda mess: 'Получить расписание' == mess.text, content_types=['text'])
def handle_text(message):
    user_markup1 = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup1.row('ЕПФ')
    user_markup1.row('Історичний')
    user_markup1.row('Філологія')
    user_markup1.row('Іноземні мови')
    bot.send_message(message.from_user.id, 'Выберите факультет:', reply_markup=user_markup1)
    
@bot.message_handler(func=lambda mess: 'ЕПФ' == mess.text or
                     'Історичний' == mess.text or 'Філологія' == mess.text or
                     'Іноземні мови' == mess.text, content_types=['text'])
def handle_text(message):
    path= message.text
    print(path)
    user_markup1 = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup1.row('1 курс', '2 курс')
    user_markup1.row('3 курс', '4 курс')
    user_markup1.row('5 курс', '6 курс')
    bot.send_message(message.from_user.id, 'Ваш курс:', reply_markup=user_markup1)
    
@bot.message_handler(func=lambda mess: '1 курс' == mess.text or '2 курс' == mess.text or '3 курс' == mess.text or '4 курс' == mess.text or '5 курс' == mess.text or '6 курс' == mess.text, content_types=['text'])
def send_daily_notifications(message):
    course= message.text
    course= course[0]
    print(course)
    time = datetime.datetime.today().strftime('%d.%m.%Y')
    print(time)
    if path != '' and course !='' and time !='':
    user_markup1 = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup1.row('Расписание на сегодня')
    user_markup1.row('Расписание на завтра')
    user_markup1.row('Расписание на неделю')
    bot.send_message(message.from_user.id, 'День:', reply_markup=user_markup1)

@bot.message_handler(func=lambda mess: 'Расписание на сегодня' == mess.text or 'Расписание на завтра' == mess.text or 'Расписание на неделю' == mess.text, content_types=['text'])    
def handle_text(message):
    if message.text=='Расписание на сегодня':
    with urllib.request.urlopen("...link...") as url:
    data = json.loads(url.read().decode())
    else:
    if message.text=='Расписание на завтра':
    
    else:
    if message.text=='Расписание на неделю':
    
    
@bot.message_handler(func=lambda mess: 'Уведомления' == mess.text, content_types=['text'])
def handle_text(message):
    user_markup1 = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup1.row('15 минут')
    user_markup1.row('30 минут')
    user_markup1.row('45 минут')
    user_markup1.row('60 минут')
    user_markup1.row('выключить')
    bot.send_message(message.from_user.id, 'Выберите предмет:', reply_markup=user_markup1)

@bot.message_handler(func=lambda mess: '15 минут' == mess.text '30 минут' == mess.text '45 минут' == mess.text '60 минут' == mess.text, content_types=['text'])
def handle_text(message):
    notif=
    bot.send_message(message.from_user.id, 'Выберите предмет:', reply_markup=user_markup1)
bot.polling()
