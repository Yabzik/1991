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

@bot.message_handler(commands=['start'])
def handle_text(message):
    user_id = str(message.from_user.id)

    if json_work_new.user_is_registered(user_id):
        bot.send_message(message.from_user.id, "С возвращением! Используйте команду /help для получения списка доступных команд.")

    else:
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Зарегестрироваться как студент')
        user_markup.row('Зарегестрироваться как преподаватель')
        bot.send_message(message.from_user.id, "Го регаться:)", reply_markup=user_markup)



@bot.message_handler(commands=['help'])
def handle_text(message):
    user_id = str(message.from_user.id)

    if json_work_new.user_is_registered(user_id):   
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

    else:
        bot.send_message(message.from_user.id, "Вы нет в базе! Давайте регаться:)")


@bot.message_handler(func=lambda mess: 'Отменить действие' == mess.text, content_types=['text'])
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
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Отменить действие')
            bot.send_message(message.from_user.id, 'Введите сообщение:', reply_markup=user_markup)

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

        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('1. Понедельник', '2. Вторник')
        user_markup.row('3. Среда', '4. Четверг')
        user_markup.row('5. Пятница', '6. Суббота')
        user_markup.row('7. Воскресенье')
        user_markup.row('Отменить действие')

        bot.send_message(message.from_user.id, 'Выберите день:', reply_markup=user_markup)
    else:
        json_work_new.update_last_user_command_t(user_id, "")
        bot.send_message(message.from_user.id, 'Отказано в доступе')


@bot.message_handler(func=lambda mess: 'Получить список своих студентов' == mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)   
    user_status = json_work_new.get_user_status(user_id)

    if user_status == 'Староста 🤠':
        headman_group = json_work_new.get_student_group(user_id)
        group_list = json_work_new.get_group_list(headman_group)
        bot.send_message(message.from_user.id, group_list)

        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Получить расписание')
        user_markup.row('Получить список своих студентов' , 'Отправить сообщение своим студентам')
        bot.send_message(message.from_user.id, 'Выберите действие:', reply_markup=user_markup)

    else:
        if suser_tatus == 'Студент 🤓':
                json_work_new.update_last_user_command_s(user_id, "")

        elif user_status == 'Учитель 👨‍🏫👩‍🏫':
            json_work_new.update_last_user_command_t(user_id, "")

        bot.send_message(message.from_user.id, "Отказано в доступе")


@bot.message_handler(func=lambda mess: 'Получить список студентов' == mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)   
    user_status = json_work_new.get_user_status(user_id)
    
    if user_status == 'Учитель 👨‍🏫👩‍🏫':
        json_work_new.update_last_user_command_t(user_id, message.text)

        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('ЕПФ')
        user_markup.row('Исторический')
        user_markup.row('Филология')
        user_markup.row('Иностранные языки')
        user_markup.row('Отменить действие')
        bot.send_message(message.from_user.id, 'Выберите факультет:', reply_markup=user_markup)

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
        user_markup1.row('Отменить действие')
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

        if len(list_of_groups):
            for name_of_group in list_of_groups:
                user_markup.row(name_of_group)          
            
            user_markup.row('Отменить действие')    
            bot.send_message(message.from_user.id, 'Выберите название группы, список студентов которой вы хотите получить', reply_markup=user_markup)
            json_work_new.update_last_bot_msg_t(user_id, 'Выберите название группы, список студентов которой вы хотите получить')

        else:
            user_markup.row('Получить список студентов')
            bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=user_markup)

    else:
        json_work_new.update_last_user_command_s(user_id, "")
        bot.send_message(message.from_user.id, "Отказано в доступе")

       
@bot.message_handler(func=lambda mess: '1. Понедельник' == mess.text or '2. Вторник' == mess.text or '3. Среда' == mess.text or '4. Четверг' == mess.text or '5. Пятница' == mess.text or '6. Суббота' == mess.text or '7. Воскресенье' == mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id) 
    user_status = json_work_new.get_user_status(user_id)

    if user_status == 'Староста 🤠' or user_status == 'Студент 🤓':
        day = message.text[0]
        timetable = json_work_new.get_timetable(user_id, user_weekday=int(day))
        bot.send_message(user_id, timetable)

        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        
        if user_status == 'Студент 🤓':
            user_markup.row('Получить расписание')

        else:
            user_markup.row('Получить расписание')
            user_markup.row('Получить список своих студентов' , 'Отправить сообщение своим студентам')

        bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=user_markup)
    
    else:
        json_work_new.update_last_user_command_t(user_id, "")
        bot.send_message(message.from_user.id, "Отказано в доступе")

@bot.message_handler(func=lambda mess: 'Отправить сообщение студентам' == mess.text , content_types=['text'])
def handle_text(message):
        user_id = str(message.from_user.id)
        user_status = json_work_new.get_user_status(user_id)

        if user_status == 'Учитель 👨‍🏫👩‍🏫':
            json_work_new.update_last_user_command_t(user_id, message.text)
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Отменить действие')
            bot.send_message(message.from_user.id, 'Введите сообщение:', reply_markup=user_markup)

        else:
            json_work_new.update_last_user_command_s(user_id, "")
            bot.send_message(message.from_user.id, "Отказано в доступе")
    

@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)
    if json_work_new.user_is_registered(user_id): 
        user_status = json_work_new.get_user_status(user_id)

        if user_status == 'Учитель 👨‍🏫👩‍🏫':
            user_command = json_work_new.get_last_user_command_t(user_id)
            bot_command = json_work_new.get_last_bot_msg_t(user_id)

        elif user_status == 'Староста 🤠':
            user_command = json_work_new.get_last_user_command_s(user_id)
    
        if user_command =='Получить список студентов' and user_status == 'Учитель 👨‍🏫👩‍🏫' and bot_command == 'Выберите название группы, список студентов которой вы хотите получить':
            student_group = message.text
            group_list = json_work_new.get_group_list(student_group)

            bot.send_message(message.from_user.id, group_list) 
            json_work_new.update_chosen_faculty(user_id, student_group)
            json_work_new.update_last_bot_msg_t(user_id, "")
            
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Получить список студентов')

            if group_list != f"Пока нет зарегестрированных студентов в нашей системе из группы {student_group} 😐":
                user_markup.row('Отправить сообщение студентам')

            else:
                json_work_new.update_chosen_faculty(user_id, "")

            bot.send_message(message.from_user.id, 'Выберите действие:', reply_markup=user_markup)

        elif user_status == 'Учитель 👨‍🏫👩‍🏫' and user_command == 'Отправить сообщение студентам':
            group = json_work_new.get_chosen_faculty(user_id)
            group_list_id = json_work_new.get_group_list_id(group)

            for student_id in group_list_id:
                teacher_initials = json_work_new.get_teacher_name_and_father_name(str(message.from_user.id))
                teacher_initials ='Преподаватель ' + teacher_initials + ' отправил сообщение студентам вашей группы:\n' + message.text
                bot.send_message(student_id, teacher_initials)

            bot.send_message(message.from_user.id, f"Ваше сообщение успешно доставлено студентам группы {group}!")

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Получить список студентов')
            bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=user_markup)

        elif user_status == 'Староста 🤠' and user_command == 'Отправить сообщение своим студентам':
            headman_group = json_work_new.get_student_group(user_id)
            group_list_id = json_work_new.get_group_list_id_for_headmen(headman_group)
            headman_text_for_students = "Староста вашей группы отправил сообщение студентам:\n" + message.text

            for student_id in group_list_id:
                bot.send_message(student_id, headman_text_for_students)
            bot.send_message(message.from_user.id, "Ваше сообщение успешно доставлено студентам вашей группы!")

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Получить расписание')
            user_markup.row('Получить список своих студентов' , 'Отправить сообщение своим студентам')
            bot.send_message(message.from_user.id, 'Выберите действие:', reply_markup=user_markup)\

        else:
            bot.send_message(message.from_user.id, 'не поняв')

    else:
        bot.send_message(message.from_user.id, "Пока не можем(")
     

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