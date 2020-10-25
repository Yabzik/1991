import telebot
from telebot import types
import time
import datetime
import urllib.request, json 
import json_work_new

bot = telebot.TeleBot("1047628795:AAHR8i8R8Nri4nVmcAyOZTackPe3jvnPk3c")
faculty = ''
course = ''
times = ''
notif = ''
status = ''
curriculum = ''
user_id = ''
groups= ''
stud_list= ''

@bot.message_handler(commands=['subject'])
def handle_text(message):
    user_id = str(message.from_user.id)   
    status= json_work_new.get_user_status(user_id) #получение ID пользователя
    status= 'Учитель 👨‍🏫👩‍'
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    if status == 'student' :
        user_markup.row('Получить расписание')
    elif status == 'starosta' :
        user_markup.row('Получить расписание')
        user_markup.row('Получить спсиок студентов')
    elif status == 'Учитель 👨‍🏫👩‍' :
        user_markup.row('Получить спиcок студентов')
        #user_markup.row('Отправить сообщение студенту')#send_msg
    bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=user_markup)
    
@bot.message_handler(func=lambda mess: 'Получить расписание' == mess.text or 'Получить спиcок студентов' == mess.text, content_types=['text'])
def handle_text(message):
    user_markup1 = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup1.row('ЕПФ')
    user_markup1.row('Исторический')
    user_markup1.row('Филилогия')
    user_markup1.row('Иностранные языки')
    bot.send_message(message.from_user.id, 'Выберите факультет:', reply_markup=user_markup1)
    
@bot.message_handler(func=lambda mess: 'ЕПФ' == mess.text or
                     'Исторический' == mess.text or 'Филилогия' == mess.text or
                     'Иностранные языки' == mess.text, content_types=['text'])
def handle_text(message):
    faculty= message.text
    print(faculty)
    user_markup1 = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup1.row('1 курс', '2 курс')
    user_markup1.row('3 курс', '4 курс')
    user_markup1.row('5 курс', '6 курс')
    bot.send_message(message.from_user.id, 'Выберите курс:', reply_markup=user_markup1)
    
@bot.message_handler(func=lambda mess: '1 курс' == mess.text or '2 курс' == mess.text or '3 курс' == mess.text or '4 курс' == mess.text or '5 курс' == mess.text or '6 курс' == mess.text, content_types=['text'])
def send_daily_notifications(message):
    course= message.text
    course= course[0]
    print(course)
    if status == 'Учитель 👨‍🏫👩‍🏫' :
        if course  and path and times :
            pass
        else:
            user_markup1 = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup1.row('1 Понедельник', '2 Вторник')
            user_markup1.row('3 Среда', '4 Четверг')
            user_markup1.row('5 Пятница', '6 Суббота')
            user_markup1.row('7 Воскресенье')
            bot.send_message(message.from_user.id, 'День:', reply_markup=user_markup1) 
    else :
        bot.send_message(message.from_user.id, 'Напишите одно или несколько названий групп')
        times = str(datetime.datetime.today().strftime('%Y'))
        times=times[2:]
        times=str(int(times)-int(course)+1)
        print(times)
        groups=json_work_new.get_list_of_group(faculty, times)    #Получение Спсика групп
        
@bot.message_handler(func=lambda mess: 'Напишите одно или несколько названий групп', content_types=['text'])
def handle_text(message):
    if course  and path :
        pass
    else:
        groups=message.text
        result = [x.strip(' ') for x in groups.split(',')]
        for i in result:
           stud_list = json_work_new.get_group_list_id(i)
    

@bot.message_handler(func=lambda mess: '1 Понедельник' == mess.text or '2 Вторник' == mess.text or '3 Среда' == mess.text or '4 Четверг' == mess.text or '5 Пятница' == mess.text or '6 Суббота' == mess.text or '7 Воскресенье' == mess.text, content_types=['text'])
def handle_text(message):
    day= message.text
    day= day[0]    
    user_id = str(message.from_user.id)  
    curriculum = json_work_new.get_timetable(id, day[0]) #получение расписания
    
#@bot.message_handler(func=lambda mess: 'Расписание на сегодня' == mess.text or 'Расписание на завтра' == mess.text or 'Расписание на неделю' == mess.text, content_types=['text'])    
#def handle_text(message):
 #   if message.text=='Расписание на сегодня':
  #  with urllib.request.urlopen("...link...") as url:
   # data = json.loads(url.read().decode())
    #else:
    #if message.text=='Расписание на завтра':
    #
    #else:
    #if message.text=='Расписание на неделю':
    
#def write():
 #   with open("json_work_file.json", "w", encoding="utf-8") as f_write:  
#@bot.message_handler(func=lambda mess: 'Уведомления' == mess.text, content_types=['text'])
#def handle_text(message):
 #   user_markup1 = telebot.types.ReplyKeyboardMarkup(True, False)
  #  user_markup1.row('15 минут')
   # user_markup1.row('30 минут')
    #user_markup1.row('45 минут')
    #user_markup1.row('60 минут')
    #user_markup1.row('выключить')
    #bot.send_message(message.from_user.id, 'Выберите предмет:', reply_markup=user_markup1)

#@bot.message_handler(func=lambda mess: '15 минут' == mess.text '30 минут' == mess.text '45 минут' == mess.text '60 минут' == mess.text, content_types=['text'])
#def handle_text(message):
 #   notif=
  #  bot.send_message(message.from_user.id, 'Выберите предмет:', reply_markup=user_markup1)
bot.polling()
input()