'''<<<<<<< HEAD
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
======='''
import telebot
from telebot import types
import time
import datetime
import urllib.request, json 
import json_work_new
import config
import scheduler_parser

bot = telebot.TeleBot("1322097005:AAGvV3aNffzGagk2u6yW-IiiK8XI4EXMxy0")
faculty = 'Филология'
course = ''
times = ''
notif = ''
curriculum = ''
user_id = ''
groups= ''
result=''
stud_list= ''
id_list= ''
starosta_info= ''

@bot.message_handler(commands=['start'])
def handle_text(message):
    user_id = str(message.from_user.id)   
    status= json_work_new.get_user_status(user_id) #получение ID пользователя
    #status= 'Учитель 👨‍🏫👩‍'
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    if status == 'Студент 🤓' :
        user_markup.row('Получить расписание')
    elif status == 'Староста 🤠' :
        user_markup.row('Получить расписание')
        user_markup.row('Получить спсиок студентов вашей группы')
    elif status == 'Учитель 👨‍🏫👩‍🏫' :
        user_markup.row('Получить спиcок студентов')
    bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=user_markup)
    
@bot.message_handler(func=lambda mess: 'Получить расписание' == mess.text or 'Получить спиcок студентов' == mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)   
    status= json_work_new.get_user_status(user_id) #получение ID пользователя
    if status == 'Учитель 👨‍🏫👩‍🏫':
        print(message.text)
        json_work_new.update_last_user_command_t(user_id, message.text)
    else:
        json_work_new.update_last_user_command_s(user_id)
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
    status = json_work_new.get_user_status(user_id) #получение ID пользователя
    faculty = message.text
    print(faculty)
    user_markup1 = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup1.row('1 курс', '2 курс')
    user_markup1.row('3 курс', '4 курс')
    user_markup1.row('5 курс', '6 курс')
    bot.send_message(message.from_user.id, 'Выберите курс:', reply_markup=user_markup1)
    
@bot.message_handler(func=lambda mess: '1 курс' == mess.text or '2 курс' == mess.text or '3 курс' == mess.text or '4 курс' == mess.text or '5 курс' == mess.text or '6 курс' == mess.text, content_types=['text'])
def send_daily_notifications(message):
    user_id = str(message.from_user.id)   
    status= json_work_new.get_user_status(user_id) #получение ID пользователя
    course= message.text
    course= course[0]
    print(course)
    print(status)
    if status != 'Учитель 👨‍🏫👩‍🏫' :
        if course  and faculty:
            pass
        else:
            user_markup1 = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup1.row('1 Понедельник', '2 Вторник')
            user_markup1.row('3 Среда', '4 Четверг')
            user_markup1.row('5 Пятница', '6 Суббота')
            user_markup1.row('7 Воскресенье')
            bot.send_message(message.from_user.id, 'Выберите день:', reply_markup=user_markup1) 
    else :
        times = str(datetime.datetime.today().strftime('%Y'))
        times=times[2:]
        #course=str(int(times)-int(course)+1)
        print(faculty, course)
        groups=json_work_new.get_list_of_group(faculty, str(course))    #Получение Спсика групп
        bot.send_message(message.from_user.id, groups)                       
        bot.send_message(message.from_user.id, 'Напишите одно или несколько названий групп')
            
@bot.message_handler(func=lambda mess: 'Получить спсиок студентов вашей группы' == mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)   
    status= json_work_new.get_user_status(user_id) #получение ID пользователя
    if status != 'Староста 🤠':
        pass
    else:
        starosta_info=json_work_new.get_student_group(str(message.from_user.id))
        bot.send_message(message.from_user.id, 'Введите сообщение вашей группе') 
        
@bot.message_handler(func=lambda mess: 'Введите сообщение вашей группе' == mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)
    status= json_work_new.get_user_status(user_id) #получение ID пользователя
    if status == 'Староста 🤠':
        pass
    else:
        id_list = json_work_new.get_group_list_id(starosta_info)
        for j in id_list:
            starosta_initials = "Староста:" + message.text
            bot.send_message(j, starosta_initials)
       
@bot.message_handler(func=lambda mess: '1 Понедельник' == mess.text or '2 Вторник' == mess.text or '3 Среда' == mess.text or '4 Четверг' == mess.text or '5 Пятница' == mess.text or '6 Суббота' == mess.text or '7 Воскресенье' == mess.text, content_types=['text'])
def handle_text(message):
    print('something')
    user_id = str(message.from_user.id) 
    status= json_work_new.get_user_status(user_id) #получение ID пользователя
    if status == 'Староста 🤠' or status == 'Студент 🤓':
        day= message.text
        day= day[0]     
        if faculty == '':
            bot.send_message(message.from_user.id, 'Выберите факультет:')
        elif times == '':
            bot.send_message(message.from_user.id, 'Выберите курс:')
        else:
            curriculum = json_work_new.get_timetable(user_id, day) #получение расписания

@bot.message_handler(func=lambda mess: 'Отправить сообщения студентам' == mess.text , content_types=['text'])
def handle_text(message):
        user_id = str(message.from_user.id)
        json_work_new.update_last_user_command_t(user_id,message.text)
        bot.send_message(message.from_user.id, 'Введите сообщение:')

@bot.message_handler(content_types=['text'])
def handle_text(message):
    global result
    user_id = str(message.from_user.id) 
    status= json_work_new.get_user_status(user_id) #получение ID пользователя
    command = json_work_new.get_last_user_command_t(user_id)
    print("something")
    print(command, status)
    if command=='Получить спиcок студентов' and status == 'Учитель 👨‍🏫👩‍🏫':
        if course and faculty:
            pass
        else:
            print("something")
            groups=message.text
            result = [x.strip(' ') for x in groups.split(',')]
            groups_list = json_work_new.get_full_group_list()
            for i in result:
                for j in groups_list:
                    if i == j:
                        stud_list = json_work_new.get_group_list(i) #получение списка студентов
                        bot.send_message(message.from_user.id, stud_list) 
                
            user_markup1 = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup1.row('Отправить сообщения студентам')
            bot.send_message(message.from_user.id, 'Выберите действие:', reply_markup=user_markup1) 
    elif command=='Отправить сообщения студентам'and status == 'Учитель 👨‍🏫👩‍🏫':
        for i in result:
            id_list = json_work_new.get_group_list_id(i)
            for j in id_list:
                teacher_initials = json_work_new.get_teacher_name_and_father_name(str(message.from_user.id))
                teacher_initials = teacher_initials + message.text
                bot.send_message(j, teacher_initials)
    else:
        print('nothing')
     

        
        
#def notify(faculty_code, year_of_study, date):
    # students = {}
    # if not year_of_study:
    #     students.update(json_work_new.find_students({'code_of_group': faculty_code}))
    # else:
    #     students.update(json_work_new.find_students({'code_of_group': faculty_code, 'year_of_study': year_of_study}))

    # print(students)

    # for telegram_id, data in students.items():
    #     curriculum = json_work_new.get_timetable(telegram_id, date)
    #     bot.send_message(telegram_id, f"👀 Изменилось расписание на {date}: {curriculum}")
 #   pass

#scheduler_parser.notify_callback = notify
#>>>>>>> 2218907434fef91d30ac9d961e5dbeab68585559
bot.polling()
input()