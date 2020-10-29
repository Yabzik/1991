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
        user_markup.row('Зарегистрироваться как студент')
        user_markup.row('Зарегистрироваться как преподаватель')
        bot.send_message(message.from_user.id, "Го регаться:)", reply_markup=user_markup)



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
            user_markup.row('Получить список студентов своей группы' , 'Отправить сообщение своим студентам')
            json_work_new.update_last_user_command_s(user_id, message.text)

        elif user_status == 'Учитель 👨‍🏫👩‍🏫' :
            user_markup.row('Получить список студентов')
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
        json_work_new.update_last_user_command_s(user_id, message.text)

    elif user_status == 'Староста 🤠' :
        user_markup.row('Получить расписание')
        user_markup.row('Получить список студентов своей группы' , 'Отправить сообщение своим студентам')
        json_work_new.update_last_user_command_s(user_id, message.text)

    elif user_status == 'Учитель 👨‍🏫👩‍🏫' :
        user_markup.row('Получить список студентов')
        json_work_new.update_last_user_command_t(user_id, message.text)
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
            user_markup.row('Получить список студентов своей группы' , 'Отправить сообщение своим студентам')
        user_markup.row('Удалить профиль')
        bot.send_message(message.from_user.id, 'Выберите действие:', reply_markup=user_markup)

    else:
        if user_status == 'Учитель 👨‍🏫👩‍🏫':
            json_work_new.update_last_user_command_t(user_id, "")

        bot.send_message(message.from_user.id, "Отказано в доступе")


@bot.message_handler(func=lambda mess: 'Получить список студентов' == mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)   
    user_status = json_work_new.get_user_status(user_id)
    
    if user_status == 'Учитель 👨‍🏫👩‍🏫':
        json_work_new.update_last_user_command_t(user_id, message.text)
        
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        for i in json_work_new.get_list_of_faculties():
            user_markup.row(i)
        user_markup.row('Отменить действие')
        bot.send_message(message.from_user.id, 'Выберите факультет:', reply_markup=user_markup)

    else:
        json_work_new.update_last_user_command_s(user_id, "")
        bot.send_message(message.from_user.id, "Отказано в доступе")
        
    
@bot.message_handler(func=lambda mess: mess.text in json_work_new.get_list_of_faculties(), content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)
    user_status = json_work_new.get_user_status(user_id)
    if json_work_new.user_is_registered(user_id): 
        user_status = json_work_new.get_user_status(user_id)
        if user_status == 'Учитель 👨‍🏫👩‍🏫':
            json_work_new.update_last_user_command_t(user_id, message.text)
            json_work_new.update_chosen_faculty(user_id, message.text)

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('1 курс', '2 курс')
            user_markup.row('3 курс', '4 курс')
            user_markup.row('5 курс', '6 курс')
            user_markup.row('Отменить действие')
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
                    user_markup.row("Назначить себя старостой")

            if dict_of_param["status"] == 'Староста 🤠':
                        user_markup.row("Назначить себя студентом")

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
    elif json_work_new.user_in_unregistered_list(user_id):
        if json_work_new.get_last_user_command_un(user_id) == "Изменить курс":   
            dict_of_param = json_work_new.get_info_about_unregistered_student_dict(user_id)
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
                    user_markup.row("Назначить себя старостой")

            if dict_of_param["status"] == 'Староста 🤠':
                        user_markup.row("Назначить себя студентом")

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
            user_markup.row('Получить список студентов своей группы' , 'Отправить сообщение своим студентам')

        user_markup.row('Удалить профиль')
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
    

@bot.message_handler(func=lambda mess: "Зарегистрироваться как преподаватель" == mess.text, content_types=['text'])
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


@bot.message_handler(func=lambda mess: "Зарегистрироваться как студент" == mess.text, content_types=['text'])
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
                                user_markup.row("Назначить себя старостой")

                        if dict_of_param["status"] == 'Староста 🤠':
                            user_markup.row("Назначить себя студентом")

                        if json_work_new.is_valid(dict_of_param):
                            user_markup.row('Завершить регистрацию')
                        user_markup.row('Отменить регистрацию')

                        bot.send_message(message.from_user.id, user_info, reply_markup=user_markup)
                        return


            if json_work_new.is_valid(dict_of_param):
                del dict_of_param["user_status"]
                dict_of_param["last_user_command"] = ''
                dict_of_param["last_bot_msg"] = ''
                if user_status == "student":
                    dict_of_param["code_of_group"] = json_work_new.get_code_of_group(dict_of_param["name_of_faculty"])
                    dict_of_param["last_user_command"] = ""
                    dict_of_param["last_bot_msg"] = ""

                    json_work_new.remove_unregistered_user(user_id)
                    text = json_work_new.add_new_student(dict_of_param, user_id)
                    bot.send_message(message.from_user.id, text)
                    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                    user_markup.row("/help")
                    bot.send_message(message.from_user.id, "Введите команду /help для получения доступных команд", reply_markup=user_markup)
                else:
                    dict_of_param["chosen_faculty"] = ""
                    json_work_new.remove_unregistered_user(user_id)
                    text = json_work_new.add_new_teacher(dict_of_param, user_id)
                    bot.send_message(message.from_user.id, text)
                    #bot.send_message(message.from_user.id, "Введите команду /help для получения доступных команд")
                    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                    user_markup.row("/help")
                    bot.send_message(message.from_user.id, "Введите команду /help для получения доступных команд", reply_markup=user_markup)


@bot.message_handler(func=lambda mess: "Удалить профиль" == mess.text, content_types=['text'])
def handler_text(message):
    user_id = str(message.from_user.id)

    if json_work_new.user_is_registered(user_id):
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row("Да, я хочу удалить свой профиль")
        user_markup.row("Нет, я случайно (или нет) нажал эту кнопку")
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

        bot.send_message(message.from_user.id, "Ваш профиль удален")
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row("/start")
        bot.send_message(message.from_user.id, "Напишите /start для регистрации", reply_markup=user_markup)


@bot.message_handler(func=lambda mess: "Нет, я случайно (или нет) нажал эту кнопку" == mess.text, content_types=['text'])
def handler_text(message):
    user_id = str(message.from_user.id)

    if json_work_new.user_is_registered(user_id):
        bot.send_message(message.from_user.id, "Вот и отлично) Напишите /help для получения списка доступных команд")


@bot.message_handler(func=lambda mess: 'Назначить себя старостой' == mess.text, content_types=['text'])
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
                        user_markup.row("Назначить себя старостой")

                if dict_of_param["status"] == 'Староста 🤠':
                        user_markup.row("Назначить себя студентом")

                if json_work_new.is_valid(dict_of_param):
                    user_markup.row('Завершить регистрацию')
                user_markup.row('Отменить регистрацию')

                bot.send_message(message.from_user.id, user_info, reply_markup=user_markup)



@bot.message_handler(func=lambda mess: 'Назначить себя студентом' == mess.text, content_types=['text'])
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
                        user_markup.row("Назначить себя старостой")

                if dict_of_param["status"] == 'Староста 🤠':
                        user_markup.row("Назначить себя студентом")

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
                        user_markup.row("Назначить себя старостой")

                if dict_of_param["status"] == 'Староста 🤠':
                        user_markup.row("Назначить себя студентом")

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
            #го регаться

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
        #dict_of_param = json_work_new.get_info_about_unregistered_student(user_id)
        json_work_new.update_last_user_command_un(user_id, message.text)
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        for course_num in range (1, 6):
            course = str(course_num) + ' курс'
            user_markup.row(course)
        user_markup.row("Вернуться на главное меню")
        bot.send_message(message.from_user.id, 'Выберите курс:', reply_markup=user_markup)
        '''if dict_of_param["student_name"] != '' and dict_of_param["student_family_name"] != '' and dict_of_param["name_of_faculty"] != '':
            dict_of_param["year_of_study"] = message.text
            json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
            groups = json_work_new.get_full_group_list()
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            for group in groups:
                user_markup.row(group)
            user_markup.row('Изменить курс')
            bot.send_message(message.from_user.id, 'Выберите группу:', reply_markup=user_markup)
        else:
            bot.send_message(message.from_user.id, 'Ошибка')'''
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
            bot.send_message(message.from_user.id, "Выберите для начала группу и факультет")

            user_info = json_work_new.get_info_about_unregistered_student(user_id)
            dict_of_param = json_work_new.get_info_about_unregistered_student_dict(user_id)

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)

            user_markup.row('Изменить имя', 'Изменить фамилию')
            user_markup.row('Изменить факультет', 'Изменить курс')
            user_markup.row('Изменить группу')
            if dict_of_param["student_group"] != '':
                if json_work_new.group_has_headmen(dict_of_param["student_group"]) and dict_of_param['status'] == 'Студент 🤓':
                    user_markup.row("Назначить себя старостой")

            if dict_of_param["status"] == 'Староста 🤠':
                        user_markup.row("Назначить себя студентом")

            if json_work_new.is_valid(dict_of_param):
                user_markup.row('Завершить регистрацию')
            user_markup.row('Отменить регистрацию')

            bot.send_message(message.from_user.id, user_info, reply_markup=user_markup)
    elif json_work_new.user_is_registered(telegram_id):
        bot.send_message(message.from_user.id, 'Вы уже зарегистрированы')          
    
    
'''@bot.message_handler(func=lambda mess: 'Зарегистрироваться'== mess.text or 'Изменить статус'== mess.text, content_types=['text'])
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
        bot.send_message(message.from_user.id, 'Вы уже истрированы') .'''    
        
@bot.message_handler(func=lambda mess: 'Отменить регистрацию' == mess.text, content_types=['text'])
def handle_text(message):
    user_id = str(message.from_user.id)

    if not json_work_new.user_is_registered(user_id):
        if json_work_new.user_in_unregistered_list(user_id):
            json_work_new.remove_unregistered_user(user_id)
            bot.send_message(message.from_user.id, "Регистрация отменена!")

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Зарегистрироваться как студент')
            user_markup.row('Зарегистрироваться как преподаватель')
            bot.send_message(message.from_user.id, "Го регаться:)", reply_markup=user_markup)
        else:
            bot.send_message(message.from_user.id, "Да вы вроде и не регались...")

            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Зарегистрироваться как студент')
            user_markup.row('Зарегистрироваться как преподаватель')
            bot.send_message(message.from_user.id, "Го регаться:)", reply_markup=user_markup)

    else:
        '''Обнуление последних команд'''
        bot.send_message(message.from_user.id, "непонел")

      
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

            if group_list != f"Пока нет зарегистрированных студентов в нашей системе из группы {student_group} 😐":
                user_markup.row('Отправить сообщение студентам')

            else:
                json_work_new.update_chosen_faculty(user_id, "")

            user_markup.row('Удалить профиль')
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
            user_markup.row('Удалить профиль')
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
            user_markup.row('Получить список студентов своей группы' , 'Отправить сообщение своим студентам')
            user_markup.row('Удалить профиль')
            bot.send_message(message.from_user.id, 'Выберите действие:', reply_markup=user_markup)

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
                            user_markup.row("Назначить себя старостой")

                    if dict_of_param["status"] == 'Староста 🤠':
                        user_markup.row("Назначить себя студентом")

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
                            user_markup.row("Назначить себя старостой")

                    if dict_of_param["status"] == 'Староста 🤠':
                        user_markup.row("Назначить себя студентом")

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
                    user_info = json_work_new.get_info_about_unregistered_student(user_id)
                    bot.send_message(message.from_user.id, user_info)
                                            
                    
                    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                    user_markup.row('Изменить имя', 'Изменить фамилию')
                    user_markup.row('Изменить факультет', 'Изменить курс')
                    user_markup.row('Изменить группу')
                    if dict_of_param["student_group"] != '':
                        if json_work_new.group_has_headmen(dict_of_param["student_group"])  and dict_of_param['status'] == 'Студент 🤓':
                            user_markup.row("Назначить себя старостой")

                    if dict_of_param["status"] == 'Староста 🤠':
                        user_markup.row("Назначить себя студентом")

                    if json_work_new.is_valid(dict_of_param):
                        user_markup.row('Завершить регистрацию')
                    user_markup.row('Отменить регистрацию')
                    bot.send_message(message.from_user.id, "Выберите пункт меню", reply_markup=user_markup)
                else:
                    bot.send_message(message.from_user.id, "Сначала заполните поля факультета и курса")
            else:
                bot.send_message(user_id, "Не понял(")
                '''Обнуление последней команды и последнего сообщения бота'''

        else:
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row('Зарегистрироваться как студент')
            user_markup.row('Зарегистрироваться как преподаватель')
            bot.send_message(message.from_user.id, "Я не понял что ты написал\nТак что го регаться:)", reply_markup=user_markup)

     

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