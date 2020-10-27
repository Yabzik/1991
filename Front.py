import telebot
from telebot import types
import time
import datetime
import urllib.request, json 
import json_work_new
import config
import scheduler_parser

bot = telebot.TeleBot(config.token)
faculty = 'Филология'
course = ''
times = ''
notif = ''
curriculum = ''
groups= ''
result=''
stud_list= ''
id_list= ''
starosta_info= ''

@bot.message_handler(commands=['help'])
def handle_text(message):
    user_id = str(message.from_user.id)   
    user_status = json_work_new.get_user_status(user_id) 

    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)

    if user_status == 'Студент 🤓' :
        user_markup.row('Получить расписание')
        json_work_new.update_last_user_command_s(user_id, message.text)

    elif user_status == 'Староста 🤠' :
        user_markup.row('Получить расписание')
        user_markup.row('Получить список своих студентов' , 'Отправить сообщение своим студентам')
        json_work_new.update_last_user_command_s(user_id, message.text)

    elif user_status == 'Учитель 👨‍🏫👩‍🏫' :
        user_markup.row('Получить список студентов')
        json_work_new.update_last_user_command_t(user_id, message.text)

    bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=user_markup)


@bot.message_handler(func=lambda mess: 'Отменить' == mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)   
    user_status = json_work_new.get_user_status(user_id)

    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)

    if user_status == 'Студент 🤓' :
        user_markup.row('Получить расписание')
        json_work_new.update_last_user_command_s(user_id, message.text)

    elif user_status == 'Староста 🤠' :
        user_markup.row('Получить расписание')
        user_markup.row('Получить список своих студентов' , 'Отправить сообщение своим студентам')
        json_work_new.update_last_user_command_s(user_id, message.text)

    elif user_status == 'Учитель 👨‍🏫👩‍🏫' :
        user_markup.row('Получить список студентов')
        json_work_new.update_last_user_command_t(user_id, message.text)

    bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=user_markup)


@bot.message_handler(func=lambda mess: 'Отправить сообщение своим студентам' == mess.text, content_types=['text'])
def handle_text(message):
        user_id = str(message.from_user.id) 
        user_status = json_work_new.get_user_status(user_id)

        if user_status == 'Староста 🤠' :
            #if last_command == 
            json_work_new.update_last_user_command_s(user_id, message.text)
            bot.send_message(message.from_user.id, 'Введите сообщение:')

        else:
            if status == 'Студент 🤓':
                json_work_new.update_last_user_command_s(user_id, "")

            elif status == 'Учитель 👨‍🏫👩‍🏫':
                json_work_new.update_last_user_command_t(user_id, "")

            bot.send_message(message.from_user.id, "Отказано в доступе")


@bot.message_handler(func=lambda mess: 'Получить расписание' == mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)
    user_status = json_work_new.get_user_status(user_id)

    if user_status == 'Студент 🤓' or user_status == 'Староста 🤠':
        json_work_new.update_last_user_command_s(user_id, message.text)

        user_markup1 = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup1.row('1. Понедельник', '2. Вторник')
        user_markup1.row('3. Среда', '4. Четверг')
        user_markup1.row('5. Пятница', '6. Суббота')
        user_markup1.row('7. Воскресенье')
        user_markup1.row('Отменить')

        bot.send_message(message.from_user.id, 'Выберите день:', reply_markup=user_markup1)
    else:
        json_work_new.update_last_user_command_t(user_id, "")
        bot.send_message(message.from_user.id, 'Отказано в доступе')


@bot.message_handler(func=lambda mess: 'Получить список своих студентов' == mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)   
    user_status = json_work_new.get_user_status(user_id)

    if status == 'Староста 🤠':
        headman_group = json_work_new.get_student_group(user_id)
        group_list = json_work_new.get_group_list(result)
        bot.send_message(message.from_user.id, group_list)

        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Получить расписание')
        user_markup.row('Получить список своих студентов' , 'Отправить сообщение своим студентам')
        bot.send_message(message.from_user.id, 'Выберите действие:', reply_markup=user_markup1)

    else:
        if status == 'Студент 🤓':
                json_work_new.update_last_user_command_s(user_id, "")

        elif status == 'Учитель 👨‍🏫👩‍🏫':
            json_work_new.update_last_user_command_t(user_id, "")

        bot.send_message(message.from_user.id, "Отказано в доступе")


@bot.message_handler(func=lambda mess: 'Получить список студентов' == mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)   
    user_status = json_work_new.get_user_status(user_id)
    
    if user_status == 'Учитель 👨‍🏫👩‍🏫':
        json_work_new.update_last_user_command_t(user_id, message.text)

        user_markup1 = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup1.row('ЕПФ')
        user_markup1.row('Исторический')
        user_markup1.row('Филология')
        user_markup1.row('Иностранные языки')
        user_markup1.row('Отменить')
        bot.send_message(message.from_user.id, 'Выберите факультет:', reply_markup=user_markup1)

    else:
        json_work_new.update_last_user_command_s(user_id, "")
        bot.send_message(message.from_user.id, "Отказано в доступе")
        
    
@bot.message_handler(func=lambda mess: 'ЕПФ' == mess.text or
                     'Исторический' == mess.text or 'Филология' == mess.text or
                     'Иностранные языки' == mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)
    user_status = json_work_new.get_user_status(user_id)

    if user_status == 'Учитель 👨‍🏫👩‍🏫':
        json_work_new.update_last_user_command_t(user_id, message.text)
        json_work_new.update_chosen_faculty(user_id, message.text)

        user_markup1 = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup1.row('1 курс', '2 курс')
        user_markup1.row('3 курс', '4 курс')
        user_markup1.row('5 курс', '6 курс')
        user_markup1.row('Отменить')
        bot.send_message(message.from_user.id, 'Выберите курс:', reply_markup=user_markup1)

    else:
        json_work_new.update_last_user_command_s(user_id, "")
        bot.send_message(message.from_user.id, "Отказано в доступе")
    
@bot.message_handler(func=lambda mess: '1 курс' == mess.text or '2 курс' == mess.text or '3 курс' == mess.text or '4 курс' == mess.text or '5 курс' == mess.text or '6 курс' == mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)   
    user_status= json_work_new.get_user_status(user_id)
    year_of_study = message.text[0]
    
    if user_status == 'Учитель 👨‍🏫👩‍🏫':
        json_work_new.update_last_user_command_t(user_id, "Получить список студентов")
        faculty = json_work_new.get_chosen_faculty(user_id)
        json_work_new.update_chosen_faculty(user_id, "")
        list_of_groups_text, list_of_groups = json_work_new.get_list_of_group(faculty, year_of_study)
        bot.send_message(message.from_user.id, list_of_groups_text)

        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        for name_of_group in list_of_groups:
            user_markup.row(name_of_group)          
            
        user_markup1.row('Отменить')    
        bot.send_message(message.from_user.id, 'Напишите название группы, студентам которой вы хотите оправить сообщение:', reply_markup=user_markup)
        json_work_new.update_last_bot_msg_t(user_id,'Напишите название группы, студентам которой вы хотите оправить сообщение:')

    else:
        json_work_new.update_last_user_command_s(user_id, "")
        bot.send_message(message.from_user.id, "Отказано в доступе")

       
@bot.message_handler(func=lambda mess: '1. Понедельник' == mess.text or '2. Вторник' == mess.text or '3. Среда' == mess.text or '4. Четверг' == mess.text or '5. Пятница' == mess.text or '6. Суббота' == mess.text or '7. Воскресенье' == mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id) 
    status= json_work_new.get_user_status(user_id) #получение ID пользователя
    if status == 'Староста 🤠' or status == 'Студент 🤓':
        day = message.text[0]
        curriculum = json_work_new.get_timetable(user_id, user_weekday=int(day))

        
        bot.send_message(user_id, curriculum)
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        if status == 'Студент 🤓':
            user_markup.row('Получить расписание')
        else:
            user_markup.row('Получить расписание')
            user_markup.row('Получить список своих студентов' , 'Отправить сообщение своим студентам')
        bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=user_markup)
        '''if faculty == '':
            bot.send_message(message.from_user.id, 'Выберите факультет:')
        elif times == '':
            bot.send_message(message.from_user.id, 'Выберите курс:')
        else:
             #получение расписания'''

@bot.message_handler(func=lambda mess: 'Отправить сообщения студентам' == mess.text , content_types=['text'])
def handle_text(message):
        user_id = str(message.from_user.id)
        #status= json_work_new.get_user_status(user_id) #получение ID пользователя
        json_work_new.update_last_user_command_t(user_id,message.text)
        bot.send_message(message.from_user.id, 'Введите сообщение:')
    

@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id) 
    status= json_work_new.get_user_status(user_id) #получение ID пользователя
    if status == 'Учитель 👨‍🏫👩‍🏫' :
        user_command = json_work_new.get_last_user_command_t(user_id)
        bot_command = json_work_new.get_last_bot_msg_t(user_id)
    elif status == 'Староста 🤠':
        user_command = json_work_new.get_last_user_command_s(user_id)
    
    if user_command=='Получить список студентов' and status == 'Учитель 👨‍🏫👩‍🏫' and bot_command == 'Напишите название группы, студентам которой вы хотите оправить сообщение:':
        group=message.text
        stud_list = json_work_new.get_group_list(group) #получение списка студентов
        bot.send_message(message.from_user.id, stud_list) 
        json_work_new.update_chosen_faculty(user_id,message.text)
            
        user_markup1 = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup1.row('Получить список студентов')
        user_markup1.row(f'Отправить сообщения студентам')
        bot.send_message(message.from_user.id, 'Выберите действие:', reply_markup=user_markup1) 
    elif status == 'Учитель 👨‍🏫👩‍🏫' and user_command == 'Отправить сообщения студентам':
        group = json_work_new.get_chosen_faculty(user_id)
        print(group)
        id_list = json_work_new.get_group_list_id(group)
        for j in id_list:
            if status == 'Учитель 👨‍🏫👩‍🏫':
                teacher_initials = json_work_new.get_teacher_name_and_father_name(str(message.from_user.id))
                teacher_initials ='Переподователь ' + teacher_initials + ' отправил студентам вашей группы: \n' + message.text
                bot.send_message(j, teacher_initials)
        bot.send_message(message.from_user.id, "Ваше сообщение доставлено студентам")
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Получить список студентов')
        bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=user_markup)

    elif status == 'Староста 🤠' and user_command == 'Отправить сообщение своим студентам':
        result=json_work_new.get_student_group(user_id)
        id_list = json_work_new.get_group_list_id(result)
        starosta_initials = "Староста: " + message.text
        for i in id_list:
            bot.send_message(i, starosta_initials)
        bot.send_message(message.from_user.id, "Ваше сообщение доставлено студентам")
        user_markup1 = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup1.row('Получить расписание')
        user_markup1.row('Получить список своих студентов' , 'Отправить сообщение своим студентам')
        bot.send_message(message.from_user.id, 'Выберите действие:', reply_markup=user_markup1)
    else:
        bot.send_message(message.from_user.id, 'не поняв')
     

def notify(faculty_code, year_of_study, date):
    students = {}
    if not year_of_study:
        students.update(json_work_new.find_students({'code_of_group': faculty_code}))
    else:
        students.update(json_work_new.find_students({'code_of_group': faculty_code, 'year_of_study': year_of_study}))

    print(students, {'code_of_group': faculty_code, 'year_of_study': year_of_study})

    for telegram_id, data in students.items():
        curriculum = json_work_new.get_timetable(telegram_id, date=date)
        bot.send_message(telegram_id, f"👀 Изменилось расписание на {date}: {curriculum}")

scheduler_parser.notify_callback = notify

bot.polling()
input()