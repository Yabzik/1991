import telebot
from telebot import types
import time
import datetime
import urllib.request, json 
import json_work_new
import config
import scheduler_parser

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def handle_text(message):
    user_id = str(message.from_user.id)

    if json_work_new.user_is_registered(user_id):
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('/help')
        bot.send_message(message.from_user.id, "С возвращением! Используйте команду /help для получения списка доступных команд.")

    else:
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Зарегистрироваться как студент 🤓')
        user_markup.row('Зарегистрироваться как преподаватель 👨‍🏫👩‍🏫')
        bot.send_message(message.from_user.id, f"Здравствуй, {message.from_user.first_name}! 😃\nИспользуй кнопки ниже, чтобы начать процесс регистрации в нашем боте👨‍💻👩‍💻", reply_markup=user_markup)


@bot.message_handler(commands=['help'])
def handle_text(message):
    user_id = str(message.from_user.id)

    if json_work_new.user_is_registered(user_id):   
        user_status = json_work_new.get_user_status(user_id) 

        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)

        if user_status == 'Студент 🤓' :
            user_markup.row('Получить расписание')
            user_markup.row('Получить список студентов своей группы')
            json_work_new.update_last_user_command_s(user_id, message.text)

        elif user_status == 'Староста 🤠' :
            user_markup.row('Получить расписание')
            user_markup.row('Получить список студентов своей группы')
            user_markup.row('Отправить сообщение своим студентам')
            user_markup.row('Отправить файл своим студентам')
            json_work_new.update_last_user_command_s(user_id, message.text)

        elif user_status == 'Учитель 👨‍🏫👩‍🏫' :
            user_markup.row('Получить список студентов')
            user_markup.row('Отправить сообщение студентам')
            user_markup.row('Отправить файл студентам')
            json_work_new.update_last_user_command_t(user_id, message.text)

        user_markup.row('Удалить профиль')
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
        user_markup.row('Получить список студентов своей группы')
        json_work_new.update_last_user_command_s(user_id, message.text)

    elif user_status == 'Староста 🤠' :
        user_markup.row('Получить расписание')
        user_markup.row('Получить список студентов своей группы')
        user_markup.row('Отправить сообщение своим студентам')
        user_markup.row('Отправить файл своим студентам')
        json_work_new.update_last_user_command_s(user_id, message.text)

    elif user_status == 'Учитель 👨‍🏫👩‍🏫' :
        user_markup.row('Получить список студентов')
        user_markup.row('Отправить сообщение студентам')
        user_markup.row('Отправить файл студентам')
        json_work_new.update_last_user_command_t(user_id, "")
        json_work_new.update_last_bot_msg_t(user_id, "")
        json_work_new.update_teacher_msg(user_id, "")
        json_work_new.update_chosen_faculty(user_id, "")
        json_work_new.update_answer_t(user_id, "")
    user_markup.row('Удалить профиль')
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


@bot.message_handler(func=lambda mess: 'Получить список студентов своей группы' == mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)   
    user_status = json_work_new.get_user_status(user_id)

    if user_status == 'Староста 🤠' or user_status == 'Студент 🤓':
        student_group = json_work_new.get_student_group(user_id)
        group_list = json_work_new.get_group_list(student_group)
        bot.send_message(message.from_user.id, group_list)

        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Получить расписание')
        if user_status == 'Студент 🤓':
            user_markup.row('Получить список студентов своей группы')
        else:
            user_markup.row('Получить список студентов своей группы' ) 
            user_markup.row('Отправить сообщение своим студентам')
            user_markup.row('Отправить файл своим студентам')
        user_markup.row('Удалить профиль')
        bot.send_message(message.from_user.id, 'Выберите действие:', reply_markup=user_markup)

    else:
        if user_status == 'Учитель 👨‍🏫👩‍🏫':
            json_work_new.update_last_user_command_t(user_id, "")

        bot.send_message(message.from_user.id, "Отказано в доступе")


@bot.message_handler(func=lambda mess: mess.text == 'Оставить эту возможность только старосте' or 'Получить список студентов' == mess.text or mess.text == "Да, студенты смогут ответить" or mess.text == "Нет, студенты не смогут овтетить", content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)   
    user_status = json_work_new.get_user_status(user_id)
    
    if user_status == 'Учитель 👨‍🏫👩‍🏫':
        if message.text == 'Получить список студентов':
            json_work_new.update_last_user_command_t(user_id, message.text)
        else:
            json_work_new.update_answer_t(user_id, message.text)
        
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        for i in json_work_new.get_list_of_faculties():
            user_markup.row(i)
        user_markup.row('Отменить действие')
        bot.send_message(message.from_user.id, 'Выберите факультет:', reply_markup=user_markup)

    else:
        json_work_new.update_last_user_command_s(user_id, "")
        bot.send_message(message.from_user.id, "Отказано в доступе")


@bot.message_handler(func=lambda mess: "Отправить сообщение студентам" == mess.text or mess.text == "Отправить файл студентам", content_types=['text'])
def handler_text(message):
    user_id = str(message.from_user.id)   
    user_status = json_work_new.get_user_status(user_id)
    
    if user_status == 'Учитель 👨‍🏫👩‍🏫':
        json_work_new.update_last_user_command_t(user_id, message.text)
        
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row("Да, студенты смогут ответить")
        user_markup.row("Нет, студенты не смогут овтетить")
        user_markup.row('Оставить эту возможность только старосте')
        user_markup.row('Отменить действие')
        bot.send_message(message.from_user.id, 'Студенты смогут ответить на ваше сообщение?', reply_markup=user_markup)

    else:
        json_work_new.update_last_user_command_s(user_id, "")
        bot.send_message(message.from_user.id, "Отказано в доступе")

        
    
@bot.message_handler(func=lambda mess: mess.text in json_work_new.get_list_of_faculties(), content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)
    
    if json_work_new.user_is_registered(user_id): 
        user_status = json_work_new.get_user_status(user_id)
        if user_status == 'Учитель 👨‍🏫👩‍🏫':
            #json_work_new.update_last_user_command_t(user_id, message.text)
            json_work_new.update_chosen_faculty(user_id, message.text)

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)

            for course_num in range (1, 7, 2):
                course = str(course_num) + ' курс'
                course_p = str(course_num + 1) + ' курс'
                user_markup.row(course, course_p)

            user_markup.row("Отменить действие")
            
            bot.send_message(message.from_user.id, 'Выберите курс:', reply_markup=user_markup)

        else:
            json_work_new.update_last_user_command_s(user_id, "")
            bot.send_message(message.from_user.id, "Отказано в доступе")
            
    elif json_work_new.user_in_unregistered_list(user_id):
        if json_work_new.get_last_user_command_un(user_id) == "Изменить факультет":
            dict_of_param = json_work_new.get_info_about_unregistered_student_dict(user_id)
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            if message.text in json_work_new.get_list_of_faculties():
                dict_of_param["name_of_faculty"] = message.text
                dict_of_param["student_group"] = ''
                dict_of_param["year_of_study"] = ''
                bot.send_message(message.from_user.id, "Отлично! Ваш факультет успешно изменен. Если вы ранее заполняли поля группа или курс, пожалуйста, заполните их заново")
                json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
            user_info = json_work_new.get_info_about_unregistered_student(user_id)
            bot.send_message(message.from_user.id, user_info)
                
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Изменить имя', 'Изменить фамилию')
            user_markup.row('Изменить факультет', 'Изменить курс')
            user_markup.row('Изменить группу')
            if dict_of_param["student_group"] != '':
                if json_work_new.group_has_headmen(dict_of_param["student_group"]) and dict_of_param['status'] == 'Студент 🤓':
                    user_markup.row("Назначить себя старостой 🤠")

            if dict_of_param["status"] == 'Староста 🤠':
                        user_markup.row("Назначить себя студентом 🤓")

            if json_work_new.is_valid(dict_of_param):
                    user_markup.row('Завершить регистрацию')
            user_markup.row('Отменить регистрацию')
            bot.send_message(message.from_user.id, "Выберите пункт меню", reply_markup=user_markup)
        
    
@bot.message_handler(func=lambda mess: '1 курс' == mess.text or '2 курс' == mess.text or '3 курс' == mess.text or '4 курс' == mess.text or '5 курс' == mess.text or '6 курс' == mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)

    if json_work_new.user_is_registered(user_id): 
        user_status= json_work_new.get_user_status(user_id)
        year_of_study = message.text[0]
        
        if user_status == 'Учитель 👨‍🏫👩‍🏫':
            #json_work_new.update_last_user_command_t(user_id, "Получить список студентов")
            faculty = json_work_new.get_chosen_faculty(user_id)
            json_work_new.update_chosen_faculty(user_id, "")
            list_of_groups_text, list_of_groups = json_work_new.get_list_of_group(faculty, year_of_study)
            bot.send_message(message.from_user.id, list_of_groups_text)
            last_teacher_command = json_work_new.get_last_user_command_t(user_id)

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)

            if len(list_of_groups):
                for name_of_group in list_of_groups:
                    user_markup.row(name_of_group)          
                
                user_markup.row('Отменить действие')

                if last_teacher_command == 'Получить список студентов':
                    bot_msg = 'Выберите название группы, список студентов которой вы хотите получить'
                elif last_teacher_command == 'Отправить сообщение студентам':
                    bot_msg = "Выберите название группы, сутдентам которой вы хотите отправить сообщение"
                elif last_teacher_command == 'Отправить файл студентам':
                    bot_msg = "Выберите название группы, сутдентам которой вы хотите отправить файл"

                bot.send_message(message.from_user.id, bot_msg, reply_markup=user_markup)
                json_work_new.update_last_bot_msg_t(user_id, bot_msg)

            else:
                user_markup.row('Получить список студентов')
                user_markup.row('Отправить сообщение студентам')
                user_markup.row('Отправить файл студентам')
                user_markup.row('Удалить профиль')
                bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=user_markup)

        else:
            json_work_new.update_last_user_command_s(user_id, "")
            bot.send_message(message.from_user.id, "Отказано в доступе")

    elif json_work_new.user_in_unregistered_list(user_id):
        if json_work_new.get_last_user_command_un(user_id) == "Изменить курс":   
            dict_of_param = json_work_new.get_info_about_unregistered_student_dict(user_id)
            if dict_of_param["name_of_faculty"] != '':
                dict_of_param["year_of_study"] = message.text[0]
                dict_of_param["student_group"] = ''
                bot.send_message(message.from_user.id, "Отлично! Ваш курс успешно изменен. Если вы ранее заполняли поля группа, пожалуйста, заполните её заново")
                json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
                user_info = json_work_new.get_info_about_unregistered_student(user_id)
                bot.send_message(message.from_user.id, user_info)

            
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Изменить имя', 'Изменить фамилию')
            user_markup.row('Изменить факультет', 'Изменить курс')
            user_markup.row('Изменить группу')

            if dict_of_param["student_group"] != '':
                if json_work_new.group_has_headmen(dict_of_param["student_group"]) and dict_of_param['status'] == 'Студент 🤓':
                    user_markup.row("Назначить себя старостой 🤠")

            if dict_of_param["status"] == 'Староста 🤠':
                        user_markup.row("Назначить себя студентом 🤓")

            if json_work_new.is_valid(dict_of_param):
                    user_markup.row('Завершить регистрацию')
            user_markup.row('Отменить регистрацию')
            bot.send_message(message.from_user.id, "Выберите пункт меню", reply_markup=user_markup)

        else:
            print("hello")

       
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
            user_markup.row('Получить список студентов своей группы')

        else:
            user_markup.row('Получить расписание')
            user_markup.row('Получить список студентов своей группы')
            user_markup.row('Отправить сообщение своим студентам')
            user_markup.row('Отправить файл своим студентам')

        user_markup.row('Удалить профиль')
        bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=user_markup)
    
    else:
        json_work_new.update_last_user_command_t(user_id, "")
        bot.send_message(message.from_user.id, "Отказано в доступе")
    

@bot.message_handler(func=lambda mess: "Зарегистрироваться как преподаватель 👨‍🏫👩‍🏫" == mess.text, content_types=['text'])
def heandle_text(message):
    user_id = str(message.from_user.id)

    if not json_work_new.user_is_registered(user_id):
        if not json_work_new.user_in_unregistered_list(user_id):
            dict_of_param = {
                "teacher_name": message.from_user.first_name,
                "teacher_family_name": message.from_user.last_name,
                "teacher_father_name": "",
                "user_status": "teacher",
                "last_user_command": "",
                "last_bot_msg": ""
            }

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)

            user_markup.row('Изменить имя', 'Изменить фамилию')
            user_markup.row('Изменить отчество')
            user_markup.row('Отменить регистрацию')

            json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
            info = json_work_new.get_info_about_unregistered_teacher(user_id)
            bot.send_message(message.from_user.id, info, reply_markup=user_markup)

        else:
            bot.send_message(message.from_user.id, "Вы уже начинали процесс регистрации")

    else:
        bot.send_message(message.from_user.id, "непонел")
        #Обнуление последних команд 


@bot.message_handler(func=lambda mess: "Изменить отчество" == mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)

    if not json_work_new.user_is_registered(user_id):
        if json_work_new.user_in_unregistered_list(user_id):
            if json_work_new.get_user_status_un(user_id) == 'teacher':
                json_work_new.update_last_user_command_un(user_id, message.text)

                user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                user_markup.row("Вернуться на главное меню")
                bot.send_message(message.from_user.id, "Введите отчество:", reply_markup=user_markup)

            else:
                json_work_new.update_last_user_command_un(user_id, "")
                user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                user_markup.row("Вернуться на главное меню")
                bot.send_message(message.from_user.id, "Вы что-то не понятное ввели", reply_markup=user_markup)

        else:
            bot.send_message(message.from_user.id, "Вы не зареганы в системе")

    else:
        #обнуление последних команд
        bot.send_message(message.from_user.id, "непонел")


@bot.message_handler(func=lambda mess: "Зарегистрироваться как студент 🤓" == mess.text, content_types=['text'])
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
                "status": "Студент 🤓",
                "user_status": "student",
                "last_user_command": "",
                "last_bot_msg": ""
            }

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Изменить имя', 'Изменить фамилию')
            user_markup.row('Изменить факультет', 'Изменить курс')
            user_markup.row('Изменить группу')
            user_markup.row('Отменить регистрацию')
            json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
            info = json_work_new.get_info_about_unregistered_student(user_id)
            bot.send_message(message.from_user.id, info, reply_markup=user_markup)

        else:
            bot.send_message(message.from_user.id, "Вы начинали процесс регистрации")

    else:
        bot.send_message(message.from_user.id, "Не понел(")


@bot.message_handler(func=lambda mess: 'Завершить регистрацию' == mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)

    if not json_work_new.user_is_registered(user_id):
        if json_work_new.user_in_unregistered_list(user_id):
            user_status = json_work_new.get_user_status_un(user_id)
            if user_status == "student":
                dict_of_param = json_work_new.get_info_about_unregistered_student_dict(user_id)

            else:
                dict_of_param = json_work_new.get_info_about_unregistered_teacher_dict(user_id)

            if user_status == "student":
                if dict_of_param["status"] == 'Староста 🤠':
                    if not json_work_new.group_has_headmen(dict_of_param["student_group"]):
                        bot.send_message(message.from_user.id, "Извините, но из вашей группы староста уже зарегистрированна в нашей системе")
                        dict_of_param['status'] = 'Студент 🤓'
                        json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
                        user_info = json_work_new.get_info_about_unregistered_student(user_id)

                        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)

                        user_markup.row('Изменить имя', 'Изменить фамилию')
                        user_markup.row('Изменить факультет', 'Изменить курс')
                        user_markup.row('Изменить группу')

                        if dict_of_param["student_group"] != '':
                            if json_work_new.group_has_headmen(dict_of_param["student_group"]) and dict_of_param['status'] == 'Студент 🤓':
                                user_markup.row("Назначить себя старостой 🤠")

                        if dict_of_param["status"] == 'Староста 🤠':
                            user_markup.row("Назначить себя студентом 🤓")

                        if json_work_new.is_valid(dict_of_param):
                            user_markup.row('Завершить регистрацию')
                        user_markup.row('Отменить регистрацию')

                        bot.send_message(message.from_user.id, user_info, reply_markup=user_markup)
                        return


            if json_work_new.is_valid(dict_of_param):
                del dict_of_param["user_status"]
                dict_of_param["last_user_command"] = ''
                dict_of_param["last_bot_msg"] = ''
                dict_of_param["last_id"] = []
                dict_of_param["answer"] = ''

                if user_status == "student":
                    dict_of_param["code_of_group"] = json_work_new.get_code_of_group(dict_of_param["name_of_faculty"])
                    dict_of_param["student_msg"] = ""

                    json_work_new.remove_unregistered_user(user_id)
                    text = json_work_new.add_new_student(dict_of_param, user_id)

                    bot.send_message(message.from_user.id, text)
                    bot.send_message(message.from_user.id, "Спасибо, что начали пользоваться нашим ботом☺️\nКоманда разработчиков надееться, что у вас будет положительный опыт использования нашего бота")
                    bot.send_message(message.from_user.id, "В знак благодарности мы даем тебе наши фирменные стикеры, которое ты можешь использовать как для коммуникации с ботом, так и для своих нужд")
                    bot.send_sticker(message.from_user.id, "CAACAgIAAxkBAAMCX5sLPFCziNQRdIwrp9crs6n4yB4AAmwJAAKzkqlINHYOQQw5FBIbBA")
                    
                    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                    user_markup.row("/help")
                    bot.send_message(message.from_user.id, "Введите команду /help для получения доступных команд", reply_markup=user_markup)
                else:
                    dict_of_param["chosen_faculty"] = ""
                    dict_of_param["teacher_msg"] = ""
                    json_work_new.remove_unregistered_user(user_id)
                    text = json_work_new.add_new_teacher(dict_of_param, user_id)

                    bot.send_message(message.from_user.id, text)
                    bot.send_message(message.from_user.id, "Спасибо, что начали пользоваться нашим ботом☺️\nКоманда разработчиков надееться, что у вас будет положительный опыт использования нашего бота")
                    bot.send_message(message.from_user.id, "В знак благодарности мы даем тебе наши фирменные стикеры, которое ты можешь использовать как для коммуникации с ботом, так и для своих нужд")
                    bot.send_sticker(message.from_user.id, "CAACAgIAAxkBAAMCX5sLPFCziNQRdIwrp9crs6n4yB4AAmwJAAKzkqlINHYOQQw5FBIbBA")
                    
                    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                    user_markup.row("/help")
                    bot.send_message(message.from_user.id, "Введите команду /help для получения доступных команд", reply_markup=user_markup)


@bot.message_handler(func=lambda mess: "Удалить профиль" == mess.text, content_types=['text'])
def handler_text(message):
    user_id = str(message.from_user.id)

    if json_work_new.user_is_registered(user_id):
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row("Да, я хочу удалить свой профиль")
        user_markup.row("Нет, я просто так нажал эту кнопку🙃")
        bot.send_message(message.from_user.id, "Вы точно хотите удалить свой профиль?", reply_markup=user_markup)


@bot.message_handler(func=lambda mess: "Да, я хочу удалить свой профиль" == mess.text, content_types=['text'])
def handler_text(message):
    user_id = str(message.from_user.id)

    if json_work_new.user_is_registered(user_id):
        user_status = json_work_new.get_user_status(user_id)

        if user_status == 'Учитель 👨‍🏫👩‍🏫':
            json_work_new.remove_teacher(user_id)
        else:
            json_work_new.remove_student(user_id)

        bot.send_message(message.from_user.id, "Ваш профиль удален😥")
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row("/start")
        bot.send_message(message.from_user.id, "Напишите /start для регистрации", reply_markup=user_markup)


@bot.message_handler(func=lambda mess: "Нет, я просто так нажал эту кнопку🙃" == mess.text, content_types=['text'])
def handler_text(message):
    user_id = str(message.from_user.id)

    if json_work_new.user_is_registered(user_id):
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row("/help")
        bot.send_message(message.from_user.id, "Вот и отлично) Напишите /help для получения списка доступных команд", reply_markup=user_markup)


@bot.message_handler(func=lambda mess: 'Назначить себя старостой 🤠' == mess.text, content_types=['text'])
def handler_text(message):
    user_id = str(message.from_user.id)

    if not json_work_new.user_is_registered(user_id):

        if json_work_new.user_in_unregistered_list(user_id):
            if json_work_new.get_user_status_un(user_id) == 'student':

                dict_of_param = json_work_new.get_info_about_unregistered_student_dict(user_id)
                dict_of_param['status'] = "Староста 🤠"

                json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
                user_info = json_work_new.get_info_about_unregistered_student(user_id)

                user_markup = telebot.types.ReplyKeyboardMarkup(True, False)

                user_markup.row('Изменить имя', 'Изменить фамилию')
                user_markup.row('Изменить факультет', 'Изменить курс')
                user_markup.row('Изменить группу')

                if dict_of_param["student_group"] != '':
                    if json_work_new.group_has_headmen(dict_of_param["student_group"]) and dict_of_param['status'] == 'Студент 🤓':
                        user_markup.row("Назначить себя старостой 🤠")

                if dict_of_param["status"] == 'Староста 🤠':
                        user_markup.row("Назначить себя студентом 🤓")

                if json_work_new.is_valid(dict_of_param):
                    user_markup.row('Завершить регистрацию')
                user_markup.row('Отменить регистрацию')

                bot.send_message(message.from_user.id, user_info, reply_markup=user_markup)


@bot.message_handler(func=lambda mess: 'Назначить себя студентом 🤓' == mess.text, content_types=['text'])
def handler_text(message):
    user_id = str(message.from_user.id)

    if not json_work_new.user_is_registered(user_id):

        if json_work_new.user_in_unregistered_list(user_id):
            if json_work_new.get_user_status_un(user_id) == 'student':

                dict_of_param = json_work_new.get_info_about_unregistered_student_dict(user_id)
                dict_of_param['status'] = "Студент 🤓"

                json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
                user_info = json_work_new.get_info_about_unregistered_student(user_id)

                user_markup = telebot.types.ReplyKeyboardMarkup(True, False)

                user_markup.row('Изменить имя', 'Изменить фамилию')
                user_markup.row('Изменить факультет', 'Изменить курс')
                user_markup.row('Изменить группу')

                if dict_of_param["student_group"] != '':
                    if json_work_new.group_has_headmen(dict_of_param["student_group"]) and dict_of_param['status'] == 'Студент 🤓':
                        user_markup.row("Назначить себя старостой 🤠")

                if dict_of_param["status"] == 'Староста 🤠':
                        user_markup.row("Назначить себя студентом 🤓")

                if json_work_new.is_valid(dict_of_param):
                    user_markup.row('Завершить регистрацию')
                user_markup.row('Отменить регистрацию')

                bot.send_message(message.from_user.id, user_info, reply_markup=user_markup)


@bot.message_handler(func=lambda mess: 'Вернуться на главное меню' == mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)

    if not json_work_new.user_is_registered(user_id):

        if json_work_new.user_in_unregistered_list(user_id):
            if json_work_new.get_user_status_un(user_id) == 'student':
                user_info = json_work_new.get_info_about_unregistered_student(user_id)
                dict_of_param = json_work_new.get_info_about_unregistered_student_dict(user_id)

                user_markup = telebot.types.ReplyKeyboardMarkup(True, False)

                user_markup.row('Изменить имя', 'Изменить фамилию')
                user_markup.row('Изменить факультет', 'Изменить курс')
                user_markup.row('Изменить группу')

                if dict_of_param["student_group"] != '':
                    if json_work_new.group_has_headmen(dict_of_param["student_group"]) and dict_of_param['status'] == 'Студент 🤓':
                        user_markup.row("Назначить себя старостой 🤠")

                if dict_of_param["status"] == 'Староста 🤠':
                        user_markup.row("Назначить себя студентом 🤓")

                if json_work_new.is_valid(dict_of_param):
                    user_markup.row('Завершить регистрацию')
                user_markup.row('Отменить регистрацию')

                bot.send_message(message.from_user.id, user_info, reply_markup=user_markup)

            else:
                user_info = json_work_new.get_info_about_unregistered_teacher(user_id)
                dict_of_param = json_work_new.get_info_about_unregistered_teacher_dict(user_id)

                user_markup = telebot.types.ReplyKeyboardMarkup(True, False)

                user_markup.row('Изменить имя', 'Изменить фамилию')
                user_markup.row('Изменить отчество')
                if json_work_new.is_valid(dict_of_param):
                    user_markup.row('Завершить регистрацию')
                user_markup.row('Отменить регистрацию')
                
                bot.send_message(message.from_user.id, user_info, reply_markup=user_markup)

    else:
        '''Обнуление последней команды и сообщения бота в зависимости от статуса'''
        bot.send_message(user_id, "не понел")

        
@bot.message_handler(func=lambda mess: 'Изменить имя' == mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)

    if not json_work_new.user_is_registered(user_id):
        if json_work_new.user_in_unregistered_list(user_id):
        
            json_work_new.update_last_user_command_un(user_id, message.text)

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row("Вернуться на главное меню")
            bot.send_message(message.from_user.id, "Введите имя:", reply_markup=user_markup)

        else:
            bot.send_message(message.from_user.id, 'Вы ещё не начинали процесс регистрации')
            #го регаться

    else:
        #обнуление команд
        bot.send_message(message.from_user.id, "непонел")
        

@bot.message_handler(func=lambda mess: "Изменить фамилию" == mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)
    
    if not json_work_new.user_is_registered(user_id):
        if json_work_new.user_in_unregistered_list(user_id):
        
            json_work_new.update_last_user_command_un(user_id, message.text)

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row("Вернуться на главное меню")
            bot.send_message(message.from_user.id, "Введите фамилию:", reply_markup=user_markup)

        else:
            bot.send_message(message.from_user.id, 'Вы ещё не начинали процесс регистрации')
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Зарегистрироваться как студент 🤓')
            user_markup.row('Зарегистрироваться как преподаватель 👨‍🏫👩‍🏫')
            bot.send_message(message.from_user.id, "Давай попробуем зарегистрироваться☺️", reply_markup=user_markup)

    else:
        #обнуление команд
        bot.send_message(message.from_user.id, "непонел")   
         

@bot.message_handler(func=lambda mess: "Изменить факультет" == mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)

    if json_work_new.user_in_unregistered_list(user_id):
        json_work_new.update_last_user_command_un(user_id, message.text)
        
        faculties = json_work_new.get_list_of_faculties()
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        for faculty in faculties:
            user_markup.row(faculty)

        user_markup.row("Вернуться на главное меню")
        bot.send_message(message.from_user.id, 'Выберите факультет:', reply_markup=user_markup)

    elif json_work_new.user_is_registered(telegram_id):
        bot.send_message(message.from_user.id, 'Вы уже зарегистрированы')         


@bot.message_handler(func=lambda mess: 'Изменить курс'== mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)

    if json_work_new.user_in_unregistered_list(user_id):
        
        json_work_new.update_last_user_command_un(user_id, message.text)
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)

        for course_num in range (1, 7, 2):
            course = str(course_num) + ' курс'
            course_p = str(course_num + 1) + ' курс'
            user_markup.row(course, course_p)

        user_markup.row("Вернуться на главное меню")
        bot.send_message(message.from_user.id, 'Выберите курс:', reply_markup=user_markup)
        
    elif json_work_new.user_is_registered(telegram_id):
        bot.send_message(message.from_user.id, 'Вы уже зарегистрированы')     
        

@bot.message_handler(func=lambda mess: 'Изменить группу'== mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)
    if json_work_new.user_in_unregistered_list(user_id):
        dict_of_param = json_work_new.get_info_about_unregistered_student_dict(user_id)
        if dict_of_param['year_of_study'] != '':
            json_work_new.update_last_user_command_un(user_id, message.text)
            groups = json_work_new.get_list_of_group(dict_of_param["name_of_faculty"], dict_of_param["year_of_study"])[1]
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            for group in groups:
                user_markup.row(group)
            user_markup.row("Вернуться на главное меню")
            bot.send_message(message.from_user.id, 'Выберите группу:', reply_markup=user_markup)
        else:
            bot.send_message(message.from_user.id, "Сначала заполните поля факультета и курса!😡")

            user_info = json_work_new.get_info_about_unregistered_student(user_id)
            dict_of_param = json_work_new.get_info_about_unregistered_student_dict(user_id)

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)

            user_markup.row('Изменить имя', 'Изменить фамилию')
            user_markup.row('Изменить факультет', 'Изменить курс')
            user_markup.row('Изменить группу')
            if dict_of_param["student_group"] != '':
                if json_work_new.group_has_headmen(dict_of_param["student_group"]) and dict_of_param['status'] == 'Студент 🤓':
                    user_markup.row("Назначить себя старостой 🤠")

            if dict_of_param["status"] == 'Староста 🤠':
                        user_markup.row("Назначить себя студентом 🤓")

            if json_work_new.is_valid(dict_of_param):
                user_markup.row('Завершить регистрацию')
            user_markup.row('Отменить регистрацию')

            bot.send_message(message.from_user.id, user_info, reply_markup=user_markup)
    elif json_work_new.user_is_registered(telegram_id):
        bot.send_message(message.from_user.id, 'Вы уже зарегистрированы')          
     
        
@bot.message_handler(func=lambda mess: 'Отменить регистрацию' == mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)

    if not json_work_new.user_is_registered(user_id):
        if json_work_new.user_in_unregistered_list(user_id):
            json_work_new.remove_unregistered_user(user_id)
            bot.send_message(message.from_user.id, "Регистрация отменена😥")

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Зарегистрироваться как студент 🤓')
            user_markup.row('Зарегистрироваться как преподаватель 👨‍🏫👩‍🏫')
            bot.send_message(message.from_user.id, "Давай опять попробуем зарегистрироваться☺️", reply_markup=user_markup)
        else:
            bot.send_message(message.from_user.id, "Да вы вроде и не регались...")

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Зарегистрироваться как студент 🤓')
            user_markup.row('Зарегистрироваться как преподаватель 👨‍🏫👩‍🏫')
            bot.send_message(message.from_user.id, "Давай попробуем зарегистрироваться☺️", reply_markup=user_markup)

    else:
        '''Обнуление последних команд'''
        bot.send_message(message.from_user.id, "непонел")


@bot.message_handler(func=lambda mess: "Отправить файл своим студентам" == mess.text, content_types=['text'])
def handler_text(message):
    user_id = str(message.from_user.id) 
    user_status = json_work_new.get_user_status(user_id)

    if user_status == 'Староста 🤠' :
        #if last_command == 
        json_work_new.update_last_user_command_s(user_id, message.text)
        json_work_new.update_last_bot_msg_s(user_id, 'Введите сообщение:')
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Отменить действие')
        bot.send_message(message.from_user.id, 'Введите сообщение:', reply_markup=user_markup)

    else:
        if status == 'Студент 🤓':
            json_work_new.update_last_user_command_s(user_id, "")

        elif status == 'Учитель 👨‍🏫👩‍🏫':
            json_work_new.update_last_user_command_t(user_id, "")
        bot.send_message(message.from_user.id, "Отказано в доступе")

      
@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)

    if json_work_new.user_is_registered(user_id): 
        user_status = json_work_new.get_user_status(user_id)

        if user_status == 'Учитель 👨‍🏫👩‍🏫':
            user_command = json_work_new.get_last_user_command_t(user_id)
            bot_command = json_work_new.get_last_bot_msg_t(user_id)

        else:
            user_command = json_work_new.get_last_user_command_s(user_id)
            bot_command = json_work_new.get_last_bot_msg_s(user_id)
    
        if user_command =='Получить список студентов' and user_status == 'Учитель 👨‍🏫👩‍🏫' and bot_command == 'Выберите название группы, список студентов которой вы хотите получить':
            student_group = message.text
            group_list = json_work_new.get_group_list(student_group)

            bot.send_message(message.from_user.id, group_list) 
            json_work_new.update_chosen_faculty(user_id, student_group)
            json_work_new.update_last_user_command_t(user_id, "")
            json_work_new.update_last_bot_msg_t(user_id, "")
            
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Получить список студентов')
            user_markup.row('Отправить сообщение студентам')
            user_markup.row('Отправить файл студентам')

            
            json_work_new.update_chosen_faculty(user_id, "")

            user_markup.row('Удалить профиль')
            bot.send_message(message.from_user.id, 'Выберите действие:', reply_markup=user_markup)

        elif user_status == 'Учитель 👨‍🏫👩‍🏫' and user_command == 'Отправить сообщение студентам' and bot_command == 'Выберите название группы, сутдентам которой вы хотите отправить сообщение':
            student_group = message.text
            json_work_new.update_chosen_faculty(user_id, student_group)
            group_list_id = json_work_new.get_group_list_id(student_group)

            if len(group_list_id):
                json_work_new.update_last_bot_msg_t(user_id, "Введите сообщение:")
                user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                user_markup.row('Отменить действие')
                bot.send_message(message.from_user.id, 'Введите сообщение:', reply_markup=user_markup)
                


            else:
                bot.send_message(message.from_user.id, f"Пока нет зарегистрированных студентов в нашей системе из группы {student_group} 😐")

                user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                user_markup.row('Получить список студентов')
                user_markup.row('Отправить сообщение студентам')
                user_markup.row('Отправить файл студентам')
                user_markup.row('Удалить профиль')
                bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=user_markup)
                json_work_new.update_last_user_command_t(user_id, "")
                json_work_new.update_last_bot_msg_t(user_id, "")
                json_work_new.update_chosen_faculty(user_id, "")

        elif user_status == 'Учитель 👨‍🏫👩‍🏫' and user_command == 'Отправить сообщение студентам' and bot_command == 'Введите сообщение:':
            teacher_msg = message.text

            student_group = json_work_new.get_chosen_faculty(user_id)
            group_list_id = json_work_new.get_group_list_id(student_group)
            answer = json_work_new.get_answer_t(user_id)
            

            for student_id in group_list_id:
                teacher_initials = json_work_new.get_teacher_name_and_father_name(str(message.from_user.id))
                teachers_msg ='Преподаватель ' + teacher_initials + ' отправил сообщение студентам вашей группы:\n' + message.text
                print(answer)
                if answer != "Нет, студенты не смогут ответить":
                    if answer == 'Оставить эту возможность только старосте' and json_work_new.user_is_headmen(str(student_id)) or answer == "Да, студенты смогут ответить":
                        keyboard = telebot.types.InlineKeyboardMarkup()
                        callback_button = telebot.types.InlineKeyboardButton(text="Ответить на сообщение", callback_data=user_id + ' ' + str(message.message_id))
                        keyboard.add(callback_button)
                        callback_button = telebot.types.InlineKeyboardButton(text="Отправить файл", callback_data='Ф' + user_id + ' ' + str(message.message_id))
                        keyboard.add(callback_button)
                        callback_button = telebot.types.InlineKeyboardButton(text="Не отвечать на сообщение", callback_data="nothing")
                        keyboard.add(callback_button)
                        bot.send_message(student_id, teachers_msg, reply_markup=keyboard)
                        print('hello')
                    else:
                        bot.send_message(student_id, teachers_msg)
                else:
                    bot.send_message(student_id, teachers_msg)


            bot.send_message(message.from_user.id, f"Ваше сообщение успешно доставлено студентам группы {student_group}!")
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Получить список студентов')
            user_markup.row('Отправить сообщение студентам')
            user_markup.row('Отправить файл студентам')
            user_markup.row('Удалить профиль')
            bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=user_markup)
            json_work_new.update_last_user_command_t(user_id, "")
            json_work_new.update_last_bot_msg_t(user_id, "")
            json_work_new.update_last_user_id_t(user_id, [])
            json_work_new.update_answer_t(user_id, "")

        elif user_status != 'Учитель 👨‍🏫👩‍🏫' and user_command == "Ответить на сообщение":
            print('ho')
            student_msg = message.text

            student_info = json_work_new.get_info_about_student_dict(user_id)
            teacher_id_info = json_work_new.get_last_user_id_s(user_id)
            if user_status == 'Староста 🤠':
                user = 'Староста'
            else:
                user = 'Студент'
            text = f"{user} группы {student_info['student_group']}, {student_info['student_family_name']} {student_info['student_name']} ответил на ваше сообщение:\n" + student_msg
            print(json_work_new.user_is_registered(teacher_id_info[0]))
            print(teacher_id_info[0])

            if json_work_new.user_is_registered(teacher_id_info[0]):            
                keyboard = telebot.types.InlineKeyboardMarkup()
                callback_button = telebot.types.InlineKeyboardButton(text="Ответить на сообщение", callback_data=user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = telebot.types.InlineKeyboardButton(text="Отправить файл", callback_data='Ф' + user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = telebot.types.InlineKeyboardButton(text="Не отвечать на сообщение", callback_data="nothing")
                keyboard.add(callback_button)
                bot.send_message(int(teacher_id_info[0]), text, reply_markup=keyboard, reply_to_message_id=int(teacher_id_info[3]))
                bot.send_message(message.from_user.id, "Ваше сообщение успешно доставлено преподавателю!")
            else:
                bot.send_message(message.from_user.id, "Преподаватель уже удален из базы😥")

            bot.edit_message_text(chat_id=message.from_user.id, message_id=int(teacher_id_info[1]), text=teacher_id_info[2])

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Получить расписание')
            if user_status == 'Староста 🤠':
                user_markup.row('Получить список студентов своей группы')
                user_markup.row('Отправить сообщение своим студентам')
                user_markup.row('Отправить файл своим студентам')
            else:
                user_markup.row('Получить список студентов своей группы')
            user_markup.row('Удалить профиль')
            bot.send_message(message.from_user.id, 'Выберите действие:', reply_markup=user_markup)
            json_work_new.update_last_user_command_s(user_id, "")
            json_work_new.update_last_bot_msg_s(user_id, "")
            json_work_new.update_last_user_id_s(user_id, [])


        elif user_status == 'Учитель 👨‍🏫👩‍🏫' and user_command == "Ответить на сообщение":
            

            teacher_initials = json_work_new.get_teacher_name_and_father_name(str(message.from_user.id))
            teacher_msg = 'Преподаватель ' + teacher_initials + ' ответил на ваше сообщение:\n' + message.text
            student_id_info = json_work_new.get_last_user_id_t(user_id)

            if json_work_new.user_is_registered(student_id_info[0]):            
                keyboard = telebot.types.InlineKeyboardMarkup()
                callback_button = telebot.types.InlineKeyboardButton(text="Ответить на сообщение", callback_data=user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = telebot.types.InlineKeyboardButton(text="Отправить файл", callback_data='Ф' + user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = telebot.types.InlineKeyboardButton(text="Не отвечать на сообщение", callback_data="nothing")
                keyboard.add(callback_button)
                bot.send_message(int(student_id_info[0]), teacher_msg, reply_markup=keyboard, reply_to_message_id=int(student_id_info[3]))
                bot.send_message(message.from_user.id, "Ваше сообщение успешно доставлено студенту!")
            else:
                bot.send_message(message.from_user.id, "Студент уже удален из базы😥")
            bot.edit_message_text(chat_id=message.from_user.id, message_id=int(student_id_info[1]), text=student_id_info[2])

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Получить список студентов')
            user_markup.row('Отправить сообщение студентам')
            user_markup.row('Отправить файл студентам')
            user_markup.row('Удалить профиль')

            bot.send_message(message.from_user.id, 'Выберите действие:', reply_markup=user_markup)
            json_work_new.update_last_user_command_t(user_id, "")
            json_work_new.update_last_bot_msg_t(user_id, "")
            json_work_new.update_last_user_id_t(user_id, [])

        elif user_status == 'Староста 🤠' and user_command == "Ответить на сообщение студента":
            print('no')
            headmen_info = json_work_new.get_info_about_student_dict(user_id)
            student_id_info = json_work_new.get_last_user_id_s(user_id)
            if json_work_new.user_is_registered(student_id_info[0]):
                headmen_msg = 'Староста из вашей группы ответил на ваше сообщение:\n' + message.text
            
                keyboard = telebot.types.InlineKeyboardMarkup()
                callback_button = telebot.types.InlineKeyboardButton(text="Ответить на сообщение", callback_data='С' + user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = telebot.types.InlineKeyboardButton(text="Отправить файл", callback_data='ФС' + user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = telebot.types.InlineKeyboardButton(text="Не отвечать на сообщение", callback_data="nothing")
                keyboard.add(callback_button)
                bot.send_message(int(student_id_info[0]), headmen_msg, reply_markup=keyboard, reply_to_message_id=int(student_id_info[3]))
                bot.send_message(message.from_user.id, "Ваше сообщение успешно доставлено студенту!")
            else:
                bot.send_message(message.from_user.id, "Студент уже удален из базы😥")

            bot.edit_message_text(chat_id=message.from_user.id, message_id=int(student_id_info[1]), text=student_id_info[2])

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Получить расписание')
            user_markup.row('Получить список студентов своей группы')
            user_markup.row('Отправить сообщение своим студентам')
            user_markup.row('Отправить файл своим студентам')
            user_markup.row('Удалить профиль')

            bot.send_message(message.from_user.id, 'Выберите действие:', reply_markup=user_markup)
            json_work_new.update_last_user_command_s(user_id, "")
            json_work_new.update_last_bot_msg_s(user_id, "")
            json_work_new.update_last_user_id_s(user_id, [])



        elif user_status == 'Староста 🤠' and user_command == 'Отправить сообщение своим студентам':
            headman_group = json_work_new.get_student_group(user_id)
            group_list_id = json_work_new.get_group_list_id_for_headmen(headman_group)
            headman_text_for_students = "Староста вашей группы отправил сообщение студентам:\n" + message.text

            if len(group_list_id):

                for student_id in group_list_id:
                    keyboard = telebot.types.InlineKeyboardMarkup()
                    callback_button = telebot.types.InlineKeyboardButton(text="Ответить на сообщение", callback_data='С' + user_id + ' ' + str(message.message_id))
                    keyboard.add(callback_button)
                    callback_button = telebot.types.InlineKeyboardButton(text="Отправить файл", callback_data='ФС' + user_id + ' ' + str(message.message_id))
                    keyboard.add(callback_button)
                    callback_button = telebot.types.InlineKeyboardButton(text="Не отвечать на сообщение", callback_data="nothing")
                    keyboard.add(callback_button)
                    bot.send_message(student_id, headman_text_for_students, reply_markup=keyboard)
                
                bot.send_message(message.from_user.id, "Ваше сообщение успешно доставлено студентам вашей группы!")
            else:
                bot.send_message(message.from_user.id, "В нашей базе студентов из вашей группы ещё нет(")

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Получить расписание')
            user_markup.row('Получить список студентов своей группы')
            user_markup.row('Отправить сообщение своим студентам')
            user_markup.row('Отправить файл своим студентам')
            user_markup.row('Удалить профиль')
            bot.send_message(message.from_user.id, 'Выберите действие:', reply_markup=user_markup)

        elif user_status == 'Студент 🤓' and user_command == 'Ответить на сообщение старосты':
            student_info = json_work_new.get_info_about_student_dict(user_id)
            headmen_id_info = json_work_new.get_last_user_id_s(user_id)
            if json_work_new.user_is_registered(headmen_id_info[0]):
                student_msg = f'Студент из вашей группы, {student_info["student_family_name"]} {student_info["student_name"]} ответил на ваше сообщение:\n' + message.text
            
                keyboard = telebot.types.InlineKeyboardMarkup()
                callback_button = telebot.types.InlineKeyboardButton(text="Ответить на сообщение", callback_data='С' + user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = telebot.types.InlineKeyboardButton(text="Отправить файл", callback_data='ФС' + user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = telebot.types.InlineKeyboardButton(text="Не отвечать на сообщение", callback_data="nothing")
                keyboard.add(callback_button)
                bot.send_message(int(headmen_id_info[0]), student_msg, reply_markup=keyboard, reply_to_message_id=int(headmen_id_info[3]))
                bot.send_message(message.from_user.id, "Ваше сообщение успешно доставлено старосте!")
            else:
                bot.send_message(message.from_user.id, "Староста уже удален из базы😥")

            bot.edit_message_text(chat_id=message.from_user.id, message_id=int(headmen_id_info[1]), text=headmen_id_info[2])

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Получить список студентов')
            user_markup.row('Получить список студентов своей группы')
            user_markup.row('Удалить профиль')

            bot.send_message(message.from_user.id, 'Выберите действие:', reply_markup=user_markup)
            json_work_new.update_last_user_command_s(user_id, "")
            json_work_new.update_last_bot_msg_s(user_id, "")
            json_work_new.update_last_user_id_s(user_id, [])

        elif user_status == 'Учитель 👨‍🏫👩‍🏫' and user_command == 'Отправить файл студентам' and bot_command == 'Выберите название группы, сутдентам которой вы хотите отправить файл':
            student_group = message.text
            json_work_new.update_chosen_faculty(user_id, student_group)
            group_list_id = json_work_new.get_group_list_id(student_group)
            json_work_new.update_last_bot_msg_t(user_id, 'Введите сообщение:')

            if len(group_list_id):
                json_work_new.update_last_bot_msg_t(user_id, "Введите сообщение:")
                user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                user_markup.row('Отменить действие')
                bot.send_message(message.from_user.id, 'Введите сообщение:', reply_markup=user_markup)
                


            else:
                bot.send_message(message.from_user.id, f"Пока нет зарегистрированных студентов в нашей системе из группы {student_group} 😐")

                user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                user_markup.row('Получить список студентов')
                user_markup.row('Отправить сообщение студентам')
                user_markup.row('Отправить файл студентам')
                user_markup.row('Удалить профиль')
                bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=user_markup)
                json_work_new.update_last_user_command_t(user_id, "")
                json_work_new.update_last_bot_msg_t(user_id, "")
                json_work_new.update_chosen_faculty(user_id, "")

        elif user_status == 'Учитель 👨‍🏫👩‍🏫' and user_command == 'Отправить файл студентам' and bot_command == 'Введите сообщение:':
            json_work_new.update_teacher_msg(user_id, message.text)

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Отменить действие')
            bot.send_message(message.from_user.id, 'Загрузите файл (он должен быть не больше 50 Мб!)', reply_markup=user_markup)

        elif user_status != 'Учитель 👨‍🏫👩‍🏫' and bot_command == 'Введите сообщение, которое прийдет вместе с вашим файлом:':
            json_work_new.update_student_msg(user_id, message.text)

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Отменить действие')
            bot.send_message(message.from_user.id, 'Загрузите файл (он должен быть не больше 50 Мб!)', reply_markup=user_markup)

        elif user_status == 'Учитель 👨‍🏫👩‍🏫' and bot_command == 'Введите сообщение, которое прийдет вместе с вашим файлом:':
            json_work_new.update_teacher_msg(user_id, message.text)

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Отменить действие')
            bot.send_message(message.from_user.id, 'Загрузите файл (он должен быть не больше 50 Мб!)', reply_markup=user_markup)



        elif user_status == 'Староста 🤠' and user_command == 'Отправить файл своим студентам' and bot_command == 'Введите сообщение:':
            json_work_new.update_student_msg(user_id, message.text)
            print(message.text)

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Отменить действие')
            bot.send_message(message.from_user.id, 'Загрузите файл (он должен быть не больше 50 Мб!)', reply_markup=user_markup)

        elif user_status == 'Староста 🤠' and user_command == 'Отправить файл студенту' or user_status == 'Студент 🤓' and user_command == 'Отправить файл старосте':
            json_work_new.update_student_msg(user_id, message.text)

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Отменить действие')
            bot.send_message(message.from_user.id, 'Загрузите файл (он должен быть не больше 50 Мб!)', reply_markup=user_markup)

            


        else:
            bot.send_message(message.from_user.id, 'не поняв')

    else:

        if json_work_new.user_in_unregistered_list(user_id):

            if json_work_new.get_last_user_command_un(user_id) == 'Изменить имя':
                name = message.text
                user_status = json_work_new.get_user_status_un(user_id)
                if user_status == 'student':
                    dict_of_param = json_work_new.get_info_about_unregistered_student_dict(user_id)
                else:
                    dict_of_param = json_work_new.get_info_about_unregistered_teacher_dict(user_id)
                if name.isalpha() == False or len(name) > 16:
                    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                    user_markup.row("Вернуться на главное меню")
                    bot.send_message(message.from_user.id, 'Введенное имя содержит недопустимые символы!', reply_markup=user_markup)

                    bot.send_message(message.from_user.id, "Введите имя:")

                elif user_status == 'student' and name.isalpha() == True and len(name)<=15:
                    name = name.capitalize()
                    dict_of_param["student_name"] = name
                    json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
                    user_info = json_work_new.get_info_about_unregistered_student(user_id)
                    bot.send_message(message.from_user.id, "Отлично! Ваше имя успешно изменено")
                    bot.send_message(message.from_user.id, user_info)
                elif len(name)<=15:
                    name = name.capitalize()
                    dict_of_param["teacher_name"] = name
                    json_work_new.add_info_about_unregistered_teacher(dict_of_param, user_id)
                    user_info = json_work_new.get_info_about_unregistered_teacher(user_id)


                    bot.send_message(message.from_user.id, "Отлично! Ваше имя успешно изменено")
                    bot.send_message(message.from_user.id, user_info)

                user_markup = telebot.types.ReplyKeyboardMarkup(True, False)

                if user_status == 'student':
                    user_info = json_work_new.get_info_about_unregistered_student(user_id)

                    user_markup.row('Изменить имя', 'Изменить фамилию')
                    user_markup.row('Изменить факультет', 'Изменить курс')
                    user_markup.row('Изменить группу')
                    if dict_of_param["student_group"] != '':
                        if json_work_new.group_has_headmen(dict_of_param["student_group"]) and dict_of_param['status'] == 'Студент 🤓':
                            user_markup.row("Назначить себя старостой 🤠")

                    if dict_of_param["status"] == 'Староста 🤠':
                        user_markup.row("Назначить себя студентом 🤓")

                    if json_work_new.is_valid(dict_of_param):
                        user_markup.row('Завершить регистрацию')
                    user_markup.row('Отменить регистрацию')

                else:
                    user_info = json_work_new.get_info_about_unregistered_teacher(user_id)

                    user_markup.row('Изменить имя', 'Изменить фамилию')
                    user_markup.row('Изменить отчество')
                    if json_work_new.is_valid(dict_of_param):
                        user_markup.row('Завершить регистрацию')
                    user_markup.row('Отменить регистрацию')

                bot.send_message(message.from_user.id, "Выберите пункт меню", reply_markup=user_markup) 
                #Обнуление последних сообщение бота!               
            elif json_work_new.get_last_user_command_un(user_id) == "Изменить фамилию":
                name = message.text
                user_status = json_work_new.get_user_status_un(user_id)
                if user_status == 'student':
                    dict_of_param = json_work_new.get_info_about_unregistered_student_dict(user_id)
                else:
                    dict_of_param = json_work_new.get_info_about_unregistered_teacher_dict(user_id)

                if name.isalpha() == False or len(name)>15:
                    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                    user_markup.row("Вернуться на главное меню")
                    bot.send_message(message.from_user.id, 'Введенная фамилия содержит недопустимые символы!', reply_markup=user_markup)

                    bot.send_message(message.from_user.id, "Введите фамилию:")         

                elif user_status == 'student' and name.isalpha() == True and len(name)<=15:
                    name = name.capitalize()
                    dict_of_param["student_family_name"] = name
                    json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
                    user_info = json_work_new.get_info_about_unregistered_student(user_id)
                    bot.send_message(message.from_user.id, "Отлично! Ваша фамилия успешно изменено")
                    bot.send_message(message.from_user.id, user_info)

                else:
                    name = name.capitalize()
                    dict_of_param["teacher_family_name"] = name
                    json_work_new.add_info_about_unregistered_teacher(dict_of_param, user_id)
                    user_info = json_work_new.get_info_about_unregistered_teacher(user_id)


                    bot.send_message(message.from_user.id, "Отлично! Ваша фамилия успешно изменено")
                    bot.send_message(message.from_user.id, user_info)

                user_markup = telebot.types.ReplyKeyboardMarkup(True, False)

                if user_status == 'student':
                    user_info = json_work_new.get_info_about_unregistered_student(user_id)

                    user_markup.row('Изменить имя', 'Изменить фамилию')
                    user_markup.row('Изменить факультет', 'Изменить курс')
                    user_markup.row('Изменить группу')

                    if dict_of_param["student_group"] != '':
                        if json_work_new.group_has_headmen(dict_of_param["student_group"]) and dict_of_param['status'] == 'Студент 🤓':
                            user_markup.row("Назначить себя старостой 🤠")

                    if dict_of_param["status"] == 'Староста 🤠':
                        user_markup.row("Назначить себя студентом 🤓")

                    if json_work_new.is_valid(dict_of_param):
                        user_markup.row('Завершить регистрацию')
                    user_markup.row('Отменить регистрацию')

                else:
                    user_info = json_work_new.get_info_about_unregistered_teacher(user_id)

                    user_markup.row('Изменить имя', 'Изменить фамилию')
                    user_markup.row('Изменить отчество')
                    if json_work_new.is_valid(dict_of_param):
                        user_markup.row('Завершить регистрацию')
                    user_markup.row('Отменить регистрацию')

                bot.send_message(message.from_user.id, "Выберите пункт меню", reply_markup=user_markup) 
                
                #Обнуление последних сообщений бота
            elif json_work_new.get_last_user_command_un(user_id) == "Изменить отчество":
                name = message.text
                user_status = json_work_new.get_user_status_un(user_id)
                dict_of_param = json_work_new.get_info_about_unregistered_teacher_dict(user_id)
                    
                if name.isalpha() == False or len(name)>15:
                    
                    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                    user_markup.row("Вернуться на главное меню")
                    bot.send_message(message.from_user.id, 'Отчество содержит недопустимые символы!', reply_markup=user_markup)

                    bot.send_message(message.from_user.id, "Введите отчество:")

                if name.isalpha() == True and len(name)<=15:
                    name = name.capitalize()
                    dict_of_param["teacher_father_name"] = name
                    json_work_new.add_info_about_unregistered_teacher(dict_of_param, user_id)
                    user_info = json_work_new.get_info_about_unregistered_teacher(user_id)


                    bot.send_message(message.from_user.id, "Отлично! Ваше отчество успешно изменено")
                    bot.send_message(message.from_user.id, user_info)

                user_markup = telebot.types.ReplyKeyboardMarkup(True, False)

                user_info = json_work_new.get_info_about_unregistered_teacher(user_id)

                user_markup.row('Изменить имя', 'Изменить фамилию')
                user_markup.row('Изменить отчество')
                if json_work_new.is_valid(dict_of_param):
                    user_markup.row('Завершить регистрацию')
                    user_markup.row('Отменить регистрацию')

                bot.send_message(message.from_user.id, "Выберите пункт меню", reply_markup=user_markup) 
                
                #Обнуление последних сообщений бота

            elif json_work_new.get_last_user_command_un(user_id) == "Изменить группу": 
                dict_of_param = json_work_new.get_info_about_unregistered_student_dict(user_id)
                if dict_of_param["name_of_faculty"] != '' and dict_of_param["year_of_study"] != '':
                    if message.text in json_work_new.get_list_of_group(dict_of_param["name_of_faculty"],dict_of_param["year_of_study"])[1]:
                        dict_of_param["student_group"] = message.text
                        json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
                        bot.send_message(message.from_user.id, "Отлично! Ваша группа успешно изменена")
                else:
                    bot.send_message(message.from_user.id, "Сначала заполните поля факультета и курса!😡")
                    
                user_info = json_work_new.get_info_about_unregistered_student(user_id)
                bot.send_message(message.from_user.id, user_info)
                                        
                user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                user_markup.row('Изменить имя', 'Изменить фамилию')
                user_markup.row('Изменить факультет', 'Изменить курс')
                user_markup.row('Изменить группу')
                if dict_of_param["student_group"] != '':
                    if json_work_new.group_has_headmen(dict_of_param["student_group"])  and dict_of_param['status'] == 'Студент 🤓':
                        user_markup.row("Назначить себя старостой 🤠")

                if dict_of_param["status"] == 'Староста 🤠':
                    user_markup.row("Назначить себя студентом 🤓")

                if json_work_new.is_valid(dict_of_param):
                    user_markup.row('Завершить регистрацию')
                user_markup.row('Отменить регистрацию')
                bot.send_message(message.from_user.id, "Выберите пункт меню", reply_markup=user_markup)
            else:
                bot.send_message(user_id, "Не понял(")
                '''Обнуление последней команды и последнего сообщения бота'''

        else:
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Зарегистрироваться как студент 🤓')
            user_markup.row('Зарегистрироваться как преподаватель 👨‍🏫👩‍🏫')
            bot.send_message(message.from_user.id, "Я не понял что ты написал\nТак что го регаться:)", reply_markup=user_markup)

'''@bot.message_handler(content_types=['stiker'])
def handler_sticker(message)'''

@bot.message_handler(content_types=['document'])
def handler_text(message):
    user_id = str(message.from_user.id)

    if json_work_new.user_is_registered(user_id):
        user_status = json_work_new.get_user_status(user_id)
        if user_status == 'Учитель 👨‍🏫👩‍🏫':
            user_command = json_work_new.get_last_user_command_t(user_id)
        else:
            user_command = json_work_new.get_last_user_command_s(user_id)

        if user_status == 'Учитель 👨‍🏫👩‍🏫':
            teacher_msg = json_work_new.get_teacher_msg(user_id)

            student_group = json_work_new.get_chosen_faculty(user_id)
            group_list_id = json_work_new.get_group_list_id(student_group)
            answer = json_work_new.get_answer_t(user_id)

            for student_id in group_list_id:
                teacher_initials = json_work_new.get_teacher_name_and_father_name(str(message.from_user.id))
                teachers_msg ='Преподаватель ' + teacher_initials + ' отправил файл студентам вашей группы:\n' + teacher_msg
                print(answer)
                if answer != "Нет, студенты не смогут ответить":
                    if answer == 'Оставить эту возможность только старосте' and json_work_new.user_is_headmen(str(student_id)) or answer == "Да, студенты смогут ответить":
                        print(answer)
                        keyboard = telebot.types.InlineKeyboardMarkup()
                        callback_button = telebot.types.InlineKeyboardButton(text="Ответить на сообщение", callback_data=user_id + ' ' + str(message.message_id))
                        keyboard.add(callback_button)
                        callback_button = telebot.types.InlineKeyboardButton(text="Отправить файл", callback_data='Ф' + user_id + ' ' + str(message.message_id))
                        keyboard.add(callback_button)
                        callback_button = telebot.types.InlineKeyboardButton(text="Не отвечать на сообщение", callback_data="nothing")
                        keyboard.add(callback_button)
                        bot.send_message(student_id, teachers_msg, reply_markup=keyboard)
                    else:
                        bot.send_message(student_id, teachers_msg)
                else:
                    bot.send_message(student_id, teachers_msg)
                bot.send_document(student_id, message.document.file_id)

            bot.send_message(message.from_user.id, f"Ваше сообщение вместе с файлом успешно доставлены студентам группы {student_group}!")
            
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Получить список студентов')
            user_markup.row('Отправить сообщение студентам')
            user_markup.row('Отправить файл студентам')
            user_markup.row('Удалить профиль')

            bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=user_markup)
            json_work_new.update_last_user_command_t(user_id, "")
            json_work_new.update_last_bot_msg_t(user_id, "")
            json_work_new.update_last_user_id_t(user_id, [])
            json_work_new.update_teacher_msg(user_id, '')
            json_work_new.update_answer_t(user_id, '')

        elif user_status == "Студент 🤓" and user_command == 'Отправить файл старосте':

            student_info = json_work_new.get_info_about_student_dict(user_id)
            headmen_id_info = json_work_new.get_last_user_id_s(user_id)
            student_msg = json_work_new.get_student_msg(user_id)
            if json_work_new.user_is_registered(headmen_id_info[0]):
                student_msg = f'Студент из вашей группы, {student_info["student_family_name"]} {student_info["student_name"]} ответил на ваше сообщение и прикрепил файл:\n' + student_msg
            
                keyboard = telebot.types.InlineKeyboardMarkup()
                callback_button = telebot.types.InlineKeyboardButton(text="Ответить на сообщение", callback_data='С' + user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = telebot.types.InlineKeyboardButton(text="Отправить файл", callback_data='ФС' + user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = telebot.types.InlineKeyboardButton(text="Не отвечать на сообщение", callback_data="nothing")
                keyboard.add(callback_button)
                bot.send_message(int(headmen_id_info[0]), student_msg, reply_markup=keyboard, reply_to_message_id=int(headmen_id_info[3]))
                bot.send_document(int(headmen_id_info[0]), message.document.file_id)
                bot.send_message(message.from_user.id, "Ваше сообщение и файл успешно доставлены старосте!")
            else:
                bot.send_message(message.from_user.id, "Староста уже удален из базы😥")

            
            bot.edit_message_text(chat_id=message.from_user.id, message_id=int(headmen_id_info[1]), text=headmen_id_info[2])
  
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Получить расписание')
            user_markup.row('Получить список студентов своей группы')
            user_markup.row('Удалить профиль')

            bot.send_message(message.from_user.id, 'Выберите действие:', reply_markup=user_markup)
            json_work_new.update_last_user_command_s(user_id, "")
            json_work_new.update_last_bot_msg_s(user_id, "")
            json_work_new.update_last_user_id_s(user_id, [])

        elif user_status != 'Учитель 👨‍🏫👩‍🏫' and json_work_new.get_last_bot_msg_s(user_id) == "Введите сообщение, которое прийдет вместе с вашим файлом:":
            student_msg = json_work_new.get_student_msg(user_id)

            student_info = json_work_new.get_info_about_student_dict(user_id)
            teacher_id_info = json_work_new.get_last_user_id_s(user_id)
            if user_status == 'Староста 🤠':
                user = 'Староста'
            else:
                user = 'Студент'

            text = f"{user} группы {student_info['student_group']}, {student_info['student_family_name']} {student_info['student_name']} ответил на ваше сообщение и прикрепил файл:\n" + student_msg

            if json_work_new.user_is_registered(teacher_id_info[0]):            
                keyboard = telebot.types.InlineKeyboardMarkup()
                callback_button = telebot.types.InlineKeyboardButton(text="Ответить на сообщение", callback_data=user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = telebot.types.InlineKeyboardButton(text="Не отвечать на сообщение", callback_data="nothing")
                keyboard.add(callback_button)
                bot.send_message(int(teacher_id_info[0]), text, reply_markup=keyboard, reply_to_message_id=int(teacher_id_info[3]))
                bot.send_message(message.from_user.id, "Ваше сообщение вместе с файлом успешно доставлены преподавателю!")
            else:
                bot.send_message(message.from_user.id, "Преподаватель уже удален из базы😥")

            bot.send_document(int(teacher_id_info[0]), message.document.file_id)

            bot.edit_message_text(chat_id=message.from_user.id, message_id=int(teacher_id_info[1]), text=teacher_id_info[2])

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Получить расписание')
            if user_status == 'Староста 🤠':
                user_markup.row('Получить список студентов своей группы')
                user_markup.row('Отправить сообщение своим студентам')
                user_markup.row('Отправить файл своим студентам')
            else:
                user_markup.row('Получить список студентов своей группы')
            user_markup.row('Удалить профиль')
            bot.send_message(message.from_user.id, 'Выберите действие:', reply_markup=user_markup)
            json_work_new.update_last_user_command_s(user_id, "")
            json_work_new.update_last_bot_msg_s(user_id, "")
            json_work_new.update_last_user_id_s(user_id, [])
            json_work_new.update_student_msg(user_id, '')

        elif user_status == 'Староста 🤠' and user_command == 'Отправить файл студенту':
            headmen_msg = json_work_new.get_student_msg(user_id)
            headmen_info = json_work_new.get_info_about_student_dict(user_id)
            headman_group = json_work_new.get_student_group(user_id)
            group_list_id = json_work_new.get_group_list_id_for_headmen(headman_group)
            headman_text_for_students = f"Староста вашей группы, {headmen_info['student_family_name']} {headmen_info['student_name']} ответил на ваше сообщение и прикрепил файл\n" + headmen_msg

            for student_id in group_list_id:
                keyboard = telebot.types.InlineKeyboardMarkup()
                callback_button = telebot.types.InlineKeyboardButton(text="Ответить на сообщение", callback_data='С' + user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = telebot.types.InlineKeyboardButton(text="Отправить файл", callback_data='Ф' + user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = telebot.types.InlineKeyboardButton(text="Не отвечать на сообщение", callback_data="nothing")
                keyboard.add(callback_button)
                bot.send_message(student_id, headman_text_for_students, reply_markup=keyboard)
                bot.send_document(student_id, message.document.file_id)

                
            bot.send_message(message.from_user.id, "Ваше сообщение и файл успешно доставлены студенту вашей группы!")

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Получить расписание')
            user_markup.row('Получить список студентов своей группы')
            user_markup.row('Отправить сообщение своим студентам')
            user_markup.row('Отправить файл своим студентам')
            user_markup.row('Удалить профиль')
            bot.send_message(message.from_user.id, 'Выберите действие:', reply_markup=user_markup)
            json_work_new.update_last_user_command_s(user_id, "")
            json_work_new.update_last_bot_msg_s(user_id, "")
            json_work_new.update_last_user_id_s(user_id, [])
            json_work_new.update_student_msg(user_id, '')

        elif user_status == 'Староста 🤠' and user_command == 'Отправить файл своим студентам':
            headmen_msg = json_work_new.get_student_msg(user_id)
            print(headmen_msg)
            headmen_info = json_work_new.get_info_about_student_dict(user_id)
            headmen_group = json_work_new.get_student_group(user_id)
            group_list_id = json_work_new.get_group_list_id_for_headmen(headmen_group)
            headman_text_for_students = f"Староста вашей группы, {headmen_info['student_family_name']} {headmen_info['student_name']} отправил вам сообщение и прикрепил файл\n" + headmen_msg

            for student_id in group_list_id:
                keyboard = telebot.types.InlineKeyboardMarkup()
                callback_button = telebot.types.InlineKeyboardButton(text="Ответить на сообщение", callback_data='С' + user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = telebot.types.InlineKeyboardButton(text="Отправить файл", callback_data='Ф' + user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = telebot.types.InlineKeyboardButton(text="Не отвечать на сообщение", callback_data="nothing")
                keyboard.add(callback_button)
                bot.send_message(student_id, headman_text_for_students, reply_markup=keyboard)
                bot.send_document(student_id, message.document.file_id)

                
            bot.send_message(message.from_user.id, "Ваше сообщение и файл успешно доставлены студентам вашей группы!")

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Получить расписание')
            user_markup.row('Получить список студентов своей группы')
            user_markup.row('Отправить сообщение своим студентам')
            user_markup.row('Отправить файл своим студентам')
            user_markup.row('Удалить профиль')
            bot.send_message(message.from_user.id, 'Выберите действие:', reply_markup=user_markup)
            json_work_new.update_last_user_command_s(user_id, "")
            json_work_new.update_last_bot_msg_s(user_id, "")
            json_work_new.update_last_user_id_s(user_id, [])
            json_work_new.update_student_msg(user_id, '')

        


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    user_id = str(call.from_user.id)

    if call.message:
        print(call.data)
        if call.data != "nothing":
            user_status = json_work_new.get_user_status(user_id)
            user_and_message_id = call.data.split()
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            print(user_status)
            if user_status != 'Учитель 👨‍🏫👩‍🏫':
                if 'С' in call.data:
            
                    if call.data[0] == 'С': # С - на русском!!!!!

                        if user_status == "Староста 🤠":
                            json_work_new.update_last_user_command_s(user_id, "Ответить на сообщение студента")
                        else:
                            json_work_new.update_last_user_command_s(user_id, "Ответить на сообщение старосты")
                        json_work_new.update_last_user_id_s(user_id, [user_and_message_id[0][1:], call.message.message_id, call.message.text, user_and_message_id[1]])
                        bot.send_message(call.from_user.id, "Введите сообщение:", reply_markup=user_markup)
                        return

                    elif call.data[0] == 'Ф':
                        if user_status == "Староста 🤠":
                            json_work_new.update_last_user_command_s(user_id, "Отправить файл студенту")
                        else:
                            json_work_new.update_last_user_command_s(user_id, "Отправить файл старосте")
                        json_work_new.update_last_user_id_s(user_id, [user_and_message_id[0][2:], call.message.message_id, call.message.text, user_and_message_id[1]])
                        bot.send_message(call.from_user.id, "Введите сообщение, которое прийдет вместе с вашим файлом:", reply_markup=user_markup)
                        return

                    else:


                        json_work_new.update_last_user_command_s(user_id, "Ответить на сообщение")
                        json_work_new.update_last_user_id_s(user_id, [user_and_message_id[0], call.message.message_id, call.message.text, user_and_message_id[1]])

                elif call.data[0][0] == 'Ф':
                    json_work_new.update_last_bot_msg_s(user_id, "Введите сообщение, которое прийдет вместе с вашим файлом:")
                    json_work_new.update_last_user_id_s(user_id, [user_and_message_id[0][1:], call.message.message_id, call.message.text, user_and_message_id[1]])
                    user_markup.row("Отменить действие")
                    bot.send_message(call.from_user.id, "Введите сообщение, которое прийдет вместе с вашим файлом:", reply_markup=user_markup)
                    return
                else:
                    json_work_new.update_last_user_command_s(user_id, "Ответить на сообщение")
                    json_work_new.update_last_user_id_s(user_id, [user_and_message_id[0], call.message.message_id, call.message.text, user_and_message_id[1]])
                    user_markup.row("Отменить действие")
                    bot.send_message(call.from_user.id, "Введите сообщение:", reply_markup=user_markup)
                    return

            else:
                
                if call.data[0][0] == 'Ф':
                    json_work_new.update_last_user_id_t(user_id, [user_and_message_id[0][1:], call.message.message_id, call.message.text, user_and_message_id[1]])
                    json_work_new.update_last_bot_msg_t(user_id, "Введите сообщение, которое прийдет вместе с вашим файлом:")
                    user_markup.row("Отменить действие")
                    bot.send_message(call.from_user.id, "Введите сообщение, которое прийдет вместе с вашим файлом:", reply_markup=user_markup)
                else:
                    json_work_new.update_last_user_id_t(user_id, [user_and_message_id[0], call.message.message_id, call.message.text, user_and_message_id[1]])
                    json_work_new.update_last_user_command_t(user_id, "Ответить на сообщение")
                    user_markup.row("Отменить действие")
                    bot.send_message(call.from_user.id, "Введите сообщение:", reply_markup=user_markup)

            
            
        else:
            bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=call.message.text)

'''@bot.message_handler(func=lambda mess:  "CAACAgIAAxkBAAMoX5xojUxJPp4CRoNdwzSri3jP1M0AAiwCAAIh7bsD0QLdh-0eCW0bBA"== mess.text, content_types=['text'])
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Перейти на Яндекс", url="http://mathprofi.ru/")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "Как быстро матешу подтянуть? Да, математика нелегкий предмет, но не переживай, ты ее поймешь! Вот тут можно быстро понять любую тему:", reply_markup=keyboard)'''

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


if __name__ == '__main__':
    bot.polling()