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
    

@bot.message_handler(func=lambda mess: "Зарегестрироваться как студент" == mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)

    if not json_work_new.user_is_registered(user_id):
        if not json_work_new.user_in_unregistered_list(user_id):
            dict_of_param = {
                "student_name": message.from_user.first_name, 
                "student_family_name": message.from_user.last_name,
                "name_of_faculty" : "",
                "year_of_study" : "",
                "student_group" : "",
                "status": ""
        }
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Добавить имя')
            bot.send_message(message.from_user.id, 'Введите имя:', reply_markup=user_markup)
            json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
            info = json_work_new.get_info_about_unregistered_student(user_id)
            bot.send_message(message.from_user.id, info)

            #добавить кнопки
        else:
            bot.send_message(message.from_user.id, "Вы уже выбирали это!")

    else:
        bot.send_message(message.from_user.id, "Не понел(")
        
@bot.message_handler(func=lambda mess: "Добавить имя" == mess.text or "Изменить имя" == mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)
    if json_work_new.user_in_unregistered_list(user_id):
        name = message.text
        dict_of_param = json_work_new.get_info_about_unregistered_student(user_id)        
        if '-' in name: 
            namelist = name.split('-')
            namelist.capitalize()
            name = '-'.join(name)
        else:
            name = name.capitalize()
        dict_of_param["student_name"] = name
        json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Добавить фамилию')
        user_markup.row('Изменить имя')
        bot.send_message(message.from_user.id, 'Введите фамилию:', reply_markup=user_markup)
    elif json_work_new.user_is_registered(telegram_id):
        bot.send_message(message.from_user.id, 'Вы уже зарегестрированы')
        

@bot.message_handler(func=lambda mess: "Добавить фамилию" == mess.text or "Изменить фамилию" == mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)
    if json_work_new.user_in_unregistered_list(user_id):
        name = message.text
        dict_of_param = json_work_new.get_info_about_unregistered_student(user_id)
        if '-' in name:
            namelist = name.split('-')
            namelist.capitalize()
            name = '-'.join(name)
        else:
            name = name.capitalize()
        dict_of_param["student_family_name"] = name
        json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
        faculties = json_work_new.get_list_of_faculties()
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        for faculty in faculties:
            user_markup.row(faculty)
        user_markup.row('Изменить фамилию')
        bot.send_message(message.from_user.id, 'Выберите факультет:', reply_markup=user_markup)
    elif json_work_new.user_is_registered(telegram_id):
        bot.send_message(message.from_user.id, 'Вы уже зарегестрированы')
         
         
@bot.message_handler(func=lambda mess: json_work_new.get_list_of_faculties() == mess.text or "Изменить факультет" == mess.text, content_types=['text'])  #хз если в хендлер можно совать функциию !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def handle_text(message):
    user_id = str(message.from_user.id)
    if json_work_new.user_in_unregistered_list(user_id):
        dict_of_param = json_work_new.get_info_about_unregistered_student(user_id)
        if dict_of_param["student_name"] != '' and dict_of_param["student_family_name"] != '':
            dict_of_param["name_of_faculty"] = message.text
            json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            for course_num in range (1, 6):
                #course = course_num.text + ' курс'
                user_markup.row(course_num.text)
            user_markup.row('Изменить факультет')
            bot.send_message(message.from_user.id, 'Выберите курс:', reply_markup=user_markup)
        else:
            bot.send_message(message.from_user.id, 'Ошибка')
    elif json_work_new.user_is_registered(telegram_id):
        bot.send_message(message.from_user.id, 'Вы уже зарегестрированы')         

@bot.message_handler(func=lambda mess: '1' == mess.text or '2' == mess.text or '3' == mess.text or '4' == mess.text or '5' == mess.text or '6' == mess.text or 'Изменить курс'== mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)
    if json_work_new.user_in_unregistered_list(user_id):
        dict_of_param = json_work_new.get_info_about_unregistered_student(user_id)
        if dict_of_param["student_name"] != '' and dict_of_param["student_family_name"] != '' and dict_of_param["name_of_faculty"] != '':
            dict_of_param["year_of_study"] = message.text
            json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
            groups = json_work_new.get_full_group_list()
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            for group in groups:
                user_markup.row(group)
            user_markup.row('Изменить курс')
            bot.send_message(message.from_user.id, 'Выберите группу:', reply_markup=user_markup)
        else:
            bot.send_message(message.from_user.id, 'Ошибка')
    elif json_work_new.user_is_registered(telegram_id):
        bot.send_message(message.from_user.id, 'Вы уже зарегестрированы')     
        

@bot.message_handler(func=lambda mess: json_work_new.get_full_group_list() == mess.text or 'Изменить группу'== mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)
    if json_work_new.user_in_unregistered_list(user_id):
        dict_of_param = json_work_new.get_info_about_unregistered_student(user_id)
        if dict_of_param["student_name"] != '' and dict_of_param["student_family_name"] != '' and dict_of_param["name_of_faculty"] != '' and dict_of_param["year_of_study"] != '':
            dict_of_param["student_group"] = message.text
            dict_of_param["status"] = 'студент'
            json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Зарегестрироваться' , 'Изменить статус')
            user_markup.row('Изменить группу')
            bot.send_message(message.from_user.id, 'Выберите действие:', reply_markup=user_markup)
        else: 
            bot.send_message(message.from_user.id, 'Ошибка')
    elif json_work_new.user_is_registered(telegram_id):
        bot.send_message(message.from_user.id, 'Вы уже зарегестрированы')          
    
    
@bot.message_handler(func=lambda mess: 'Зарегестрироваться'== mess.text or 'Изменить статус'== mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)
    if json_work_new.user_in_unregistered_list(user_id):
        dict_of_param = json_work_new.get_info_about_unregistered_student(user_id)
        if dict_of_param["student_name"] != '' and dict_of_param["student_family_name"] != '' and dict_of_param["name_of_faculty"] != '' and dict_of_param["year_of_study"] != '' and dict_of_param["student_group"] != '' and dict_of_param["status"] == 'студент':
            if message.text == 'Изменить статус' :
                bot.send_message(message.from_user.id, 'Введите токен для получения статуса')    #Тут нужно запомнить сообщение бота но я не знаю будет ли работать функция update_last_bot_msg_s с незареганым студентом !!!!!!!!!!!!!!!
            else:
                status=json_work_new.add_new_student(dict_of_param, user_id)
                bot.send_message(message.from_user.id, status)
        else: 
            bot.send_message(message.from_user.id, 'Ошибка')
    elif json_work_new.user_is_registered(telegram_id):
        bot.send_message(message.from_user.id, 'Вы уже зарегестрированы')     
        
        
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
            bot.send_message(message.from_user.id, 'Выберите действие:', reply_markup=user_markup)

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