#import telebot
#from telebot import types
import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import logging
import time
import datetime
import urllib.request, json 
import json_work_new
import config
import scheduler_parser
import random
import string
#message.text
#message.chat.id
logging.basicConfig(level=logging.INFO)
bot = aiogram.Bot('1047628795:AAHR8i8R8Nri4nVmcAyOZTackPe3jvnPk3c')
#bot = telebot.TeleBot('1047628795:AAHR8i8R8Nri4nVmcAyOZTackPe3jvnPk3c')

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

'''@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    #user_id = str(message.chat.id)
    user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    user_markup.add('help')
    
    #await bot.send_message( message.chat.id,"С возвращением! Используйте команду /help для получения списка доступных команд.",  reply_markup=user_markup)   
    await bot.send_message( message.chat.id, message.chat.first_name,  reply_markup=user_markup)  
    #await bot.send_message( message.chat.id,"С возвращением! Используйте команду /help для получения списка доступных команд.")  '''
    
@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)

    if json_work_new.user_is_registered(user_id):
        #user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        #user_markup.add('/help')
        await bot.send_message( message.chat.id,"С возвращением! Используйте команду /help для получения списка доступных команд.")

    else:
        user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        user_markup.add('Зарегистрироваться как студент 🤓')
        user_markup.add('Зарегистрироваться как преподаватель 👨‍🏫👩‍🏫')
        await bot.send_message( message.chat.id,f"Здравствуй, {message.chat.first_name}! 😃\nИспользуй кнопки ниже, чтобы начать процесс регистрации в нашем боте👨‍💻👩‍💻", reply_markup=user_markup) 

@dp.message_handler(commands='help')
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)

    if json_work_new.user_is_registered(user_id):   
        user_status = json_work_new.get_user_status(user_id) 

        user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

        if user_status == 'Студент 🤓' :
            user_markup.add('Получить расписание')
            user_markup.add('Получить список студентов своей группы')
            json_work_new.update_last_user_command_s(user_id, message.text)

        elif user_status == 'Староста 🤠' :
            user_markup.add('Получить расписание')
            user_markup.add('Получить список студентов своей группы')
            user_markup.add('Отправить сообщение своим студентам')
            user_markup.add('Отправить файл своим студентам')
            user_markup.add('Изменить расписание')
            json_work_new.update_last_user_command_s(user_id, message.text)

        elif user_status == 'Учитель 👨‍🏫👩‍🏫' :
            user_markup.add('Получить список студентов')
            user_markup.add('Отправить сообщение студентам')
            user_markup.add('Отправить файл студентам')
            json_work_new.update_last_user_command_t(user_id, message.text)

        user_markup.add('Задать вопрос или сообщить об ошибке')
        user_markup.add('Удалить профиль')
        await bot.send_message( message.chat.id,'Выберите пункт меню:', reply_markup=user_markup)

    else:
        if json_work_new.user_in_unregistered_list(user_id):
            if json_work_new.get_user_status_un(user_id) == 'student':
                user_info = json_work_new.get_info_about_unregistered_student(user_id)
                dict_of_param = json_work_new.get_info_about_unregistered_student_dict(user_id)

                user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

                user_markup.add('Изменить имя', 'Изменить фамилию')
                user_markup.add('Изменить факультет', 'Изменить курс')
                user_markup.add('Изменить группу')

                if dict_of_param["student_group"] != '':
                    if json_work_new.group_has_headmen(dict_of_param["student_group"]) and dict_of_param['status'] == 'Студент 🤓':
                        user_markup.add("Назначить себя старостой 🤠")

                if dict_of_param["status"] == 'Староста 🤠':
                        user_markup.add("Назначить себя студентом 🤓")

                if json_work_new.is_valid(dict_of_param):
                    user_markup.add('Завершить регистрацию')
                    
                user_markup.add('Задать вопрос или сообщить об ошибке')
                user_markup.add('Отменить регистрацию')

                await bot.send_message( message.chat.id,user_info, reply_markup=user_markup)

            else:
                user_info = json_work_new.get_info_about_unregistered_teacher(user_id)
                dict_of_param = json_work_new.get_info_about_unregistered_teacher_dict(user_id)

                user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

                user_markup.add('Изменить имя', 'Изменить фамилию')
                user_markup.add('Изменить отчество')
                if json_work_new.is_valid(dict_of_param):
                    user_markup.add('Завершить регистрацию')
                    
                user_markup.add('Задать вопрос или сообщить об ошибке')
                user_markup.add('Отменить регистрацию')
                
                await bot.send_message( message.chat.id,user_info, reply_markup=user_markup)
        else:
            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            user_markup.add('Зарегистрироваться как студент 🤓')
            user_markup.add('Зарегистрироваться как преподаватель 👨‍🏫👩‍🏫')
            await bot.send_message( message.chat.id,"Вас нет в базе! Давайте регаться:)", reply_markup=user_markup) 
            

@dp.message_handler(lambda message: message.text== 'Отменить действие')
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)
    user_status = json_work_new.get_user_status(user_id)

    user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    if user_status == 'Студент 🤓' :
        user_markup.add('Получить расписание')
        user_markup.add('Получить список студентов своей группы')
        json_work_new.update_last_user_command_s(user_id, message.text)

    elif user_status == 'Староста 🤠' :
        user_markup.add('Получить расписание')
        user_markup.add('Получить список студентов своей группы')
        user_markup.add('Отправить сообщение своим студентам')
        user_markup.add('Отправить файл своим студентам')
        user_markup.add('Изменить расписание')
        json_work_new.update_last_user_command_s(user_id, message.text)

    elif user_status == 'Учитель 👨‍🏫👩‍🏫' :
        user_markup.add('Получить список студентов')
        user_markup.add('Отправить сообщение студентам')
        user_markup.add('Отправить файл студентам')
        json_work_new.update_last_user_command_t(user_id, "")
        json_work_new.update_last_bot_msg_t(user_id, "")
        json_work_new.update_teacher_msg(user_id, "")
        json_work_new.update_chosen_faculty(user_id, "")
        json_work_new.update_answer_t(user_id, "")
    user_markup.add('Задать вопрос или сообщить об ошибке')
    user_markup.add('Удалить профиль')
    await bot.send_message( message.chat.id,'Выберите пункт меню:', reply_markup=user_markup)


@dp.message_handler(lambda message: message.text== 'Отправить сообщение своим студентам')
async def cmd_start(message: types.Message):
        user_id = str(message.chat.id) 
        user_status = json_work_new.get_user_status(user_id)

        if user_status == 'Староста 🤠' :
            #if last_command == 
            json_work_new.update_last_user_command_s(user_id, message.text)
            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            user_markup.add('Отменить действие')
            await bot.send_message( message.chat.id,'Введите сообщение:', reply_markup=user_markup)

        else:
            if user_status == 'Студент 🤓':
                json_work_new.update_last_user_command_s(user_id, "")

            elif user_status == 'Учитель 👨‍🏫👩‍🏫':
                json_work_new.update_last_user_command_t(user_id, "")

            await bot.send_message( message.chat.id,"Отказано в доступе")
            
            
@dp.message_handler(lambda message: message.text== 'Задать вопрос или сообщить об ошибке')
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)
    if json_work_new.user_is_registered(user_id):
        user_status = json_work_new.get_user_status(user_id)
        if user_status != 'Учитель 👨‍🏫👩‍🏫':
            json_work_new.update_last_user_command_s(user_id, 'Задать вопрос или сообщить об ошибке')
        else:
            json_work_new.update_last_user_command_t(user_id, 'Задать вопрос или сообщить об ошибке')
        await bot.send_message( message.chat.id,"Введите сообшение, которое будет доставлено разработчику:")
    else:
        json_work_new.update_last_user_command_un(user_id, 'Задать вопрос или сообщить об ошибке')
        await bot.send_message( message.chat.id,"Введите сообшение, которое будет доставлено разработчику:")
        
        
@dp.message_handler(lambda message: message.text== 'Получить расписание' )
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)
    user_status = json_work_new.get_user_status(user_id)

    if user_status == 'Студент 🤓' or user_status == 'Староста 🤠':
        json_work_new.update_last_user_command_s(user_id, message.text)

        user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        user_markup.add('1. Понедельник', '2. Вторник')
        user_markup.add('3. Среда', '4. Четверг')
        user_markup.add('5. Пятница', '6. Суббота')
        user_markup.add('7. Воскресенье')
        user_markup.add('Отменить действие')

        await bot.send_message( message.chat.id,'Выберите день:', reply_markup=user_markup)
    else:
        json_work_new.update_last_user_command_t(user_id, "")
        await bot.send_message( message.chat.id,'Отказано в доступе')
        
        
@dp.message_handler(lambda message: message.text== 'Получить список студентов своей группы' )
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)   
    user_status = json_work_new.get_user_status(user_id)

    if user_status == 'Староста 🤠' or user_status == 'Студент 🤓':
        student_group = json_work_new.get_student_group(user_id)
        group_list = json_work_new.get_group_list(student_group)
        await bot.send_message( message.chat.id,group_list)

        user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        user_markup.add('Получить расписание')
        if user_status == 'Студент 🤓':
            user_markup.add('Получить список студентов своей группы')
        else:
            user_markup.add('Получить список студентов своей группы' ) 
            user_markup.add('Отправить сообщение своим студентам')
            user_markup.add('Отправить файл своим студентам')
            user_markup.add('Изменить расписание')
        user_markup.add('Задать вопрос или сообщить об ошибке')
        user_markup.add('Удалить профиль')
        await bot.send_message( message.chat.id,'Выберите действие:', reply_markup=user_markup)

    else:
        if user_status == 'Учитель 👨‍🏫👩‍🏫':
            json_work_new.update_last_user_command_t(user_id, "")

        await bot.send_message( message.chat.id,"Отказано в доступе")


@dp.message_handler(lambda message: message.text == 'Оставить эту возможность только старосте' or message.text == 'Получить список студентов' or message.text == "Да, студенты смогут ответить" or message.text == "Нет, студенты не смогут овтетить" )
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)   
    user_status = json_work_new.get_user_status(user_id)
    
    if user_status == 'Учитель 👨‍🏫👩‍🏫':
        if message.text == 'Получить список студентов':
            json_work_new.update_last_user_command_t(user_id, message.text)
        else:
            json_work_new.update_answer_t(user_id, message.text)
        
        user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        for i in json_work_new.get_list_of_faculties():
            user_markup.add(i)
        user_markup.add('Отменить действие')
        await bot.send_message( message.chat.id, 'Выберите факультет:', reply_markup=user_markup)

    else:
        json_work_new.update_last_user_command_s(user_id, "")
        await bot.send_message( message.chat.id, "Отказано в доступе")
       
       
@dp.message_handler(lambda message: message.text == "Отправить сообщение студентам" or message.text == "Отправить файл студентам")
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)      
    user_status = json_work_new.get_user_status(user_id)
    
    if user_status == 'Учитель 👨‍🏫👩‍🏫':
        json_work_new.update_last_user_command_t(user_id, message.text)
        
        user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        user_markup.add("Да, студенты смогут ответить")
        user_markup.add("Нет, студенты не смогут овтетить")
        user_markup.add('Оставить эту возможность только старосте')
        user_markup.add('Отменить действие')
        await bot.send_message( message.chat.id,'Студенты смогут ответить на ваше сообщение?', reply_markup=user_markup)

    else:
        json_work_new.update_last_user_command_s(user_id, "")
        await bot.send_message( message.chat.id, "Отказано в доступе")
        
        
@dp.message_handler(lambda message: message.text in json_work_new.get_list_of_faculties())
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)  
    
    if json_work_new.user_is_registered(user_id): 
        user_status = json_work_new.get_user_status(user_id)
        if user_status == 'Учитель 👨‍🏫👩‍🏫':
            #json_work_new.update_last_user_command_t(user_id, message.text)
            json_work_new.update_chosen_faculty(user_id, message.text)

            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

            for course_num in range (1, 7, 2):
                course = str(course_num) + ' курс'
                course_p = str(course_num + 1) + ' курс'
                user_markup.add(course, course_p)

            user_markup.add("Отменить действие")
            
            await bot.send_message( message.chat.id,  'Выберите курс:', reply_markup=user_markup)

        else:
            json_work_new.update_last_user_command_s(user_id, "")
            await bot.send_message( message.chat.id,"Отказано в доступе")
            
    elif json_work_new.user_in_unregistered_list(user_id):
        if json_work_new.get_last_user_command_un(user_id) == "Изменить факультет":
            dict_of_param = json_work_new.get_info_about_unregistered_student_dict(user_id)
            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            if message.text in json_work_new.get_list_of_faculties():
                dict_of_param["name_of_faculty"] = message.text
                dict_of_param["student_group"] = ''
                dict_of_param["year_of_study"] = ''
                await bot.send_message( message.chat.id,"Отлично! Ваш факультет успешно изменен. Если вы ранее заполняли поля группа или курс, пожалуйста, заполните их заново")
                json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
            user_info = json_work_new.get_info_about_unregistered_student(user_id)
            await bot.send_message( message.chat.id,user_info)
                
            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            user_markup.add('Изменить имя', 'Изменить фамилию')
            user_markup.add('Изменить факультет', 'Изменить курс')
            user_markup.add('Изменить группу')
            if dict_of_param["student_group"] != '':
                if json_work_new.group_has_headmen(dict_of_param["student_group"]) and dict_of_param['status'] == 'Студент 🤓':
                    user_markup.add("Назначить себя старостой 🤠")

            if dict_of_param["status"] == 'Староста 🤠':
                        user_markup.add("Назначить себя студентом 🤓")

            if json_work_new.is_valid(dict_of_param):
                    user_markup.add('Завершить регистрацию')
            user_markup.add('Задать вопрос или сообщить об ошибке')
            user_markup.add('Отменить регистрацию')
            await bot.send_message( message.chat.id, "Выберите пункт меню", reply_markup=user_markup)
           

@dp.message_handler(lambda message: message.text == '1 курс' or message.text == '2 курс' or message.text == '3 курс' or message.text == '4 курс' or message.text == '5 курс' or message.text == '6 курс')
async def cmd_start(message: types.Message):     
    user_id = str(message.chat.id)  

    if json_work_new.user_is_registered(user_id): 
        user_status= json_work_new.get_user_status(user_id)
        year_of_study = message.text[0]
        
        if user_status == 'Учитель 👨‍🏫👩‍🏫':
            
            faculty = json_work_new.get_chosen_faculty(user_id)
            json_work_new.update_chosen_faculty(user_id, "")
            list_of_groups_text, list_of_groups = json_work_new.get_list_of_group(faculty, year_of_study)
            await bot.send_message( message.chat.id,list_of_groups_text)
            last_teacher_command = json_work_new.get_last_user_command_t(user_id)

            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

            if len(list_of_groups):
                for name_of_group in list_of_groups:
                    user_markup.add(name_of_group)          
                
                user_markup.add('Отменить действие')

                if last_teacher_command == 'Получить список студентов':
                    bot_msg = 'Выберите название группы, список студентов которой вы хотите получить'
                    json_work_new.update_last_user_command_t(user_id, "Получить список студентов")
                elif last_teacher_command == 'Отправить сообщение студентам':
                    bot_msg = "Выберите название группы, сутдентам которой вы хотите отправить сообщение"
                    json_work_new.update_last_user_command_t(user_id, 'Отправить сообщение студентам')
                elif last_teacher_command == 'Отправить файл студентам':
                    bot_msg = "Выберите название группы, сутдентам которой вы хотите отправить файл"
                    json_work_new.update_last_user_command_t(user_id, 'Отправить файл студентам')

                await bot.send_message( message.chat.id,bot_msg, reply_markup=user_markup)
                json_work_new.update_last_bot_msg_t(user_id, bot_msg)
                bot_msg=''

            else:
                user_markup.add('Получить список студентов')
                user_markup.add('Отправить сообщение студентам')
                user_markup.add('Отправить файл студентам')
                user_markup.add('Задать вопрос или сообщить об ошибке')
                user_markup.add('Удалить профиль')
                await bot.send_message( message.chat.id,'Выберите действие', reply_markup=user_markup)

        else:
            json_work_new.update_last_user_command_s(user_id, "")
            await bot.send_message( message.chat.id,"Отказано в доступе")

    elif json_work_new.user_in_unregistered_list(user_id):
        if json_work_new.get_last_user_command_un(user_id) == "Изменить курс":   
            dict_of_param = json_work_new.get_info_about_unregistered_student_dict(user_id)
            if dict_of_param["name_of_faculty"] != '':
                dict_of_param["year_of_study"] = message.text[0]
                dict_of_param["student_group"] = ''
                await bot.send_message( message.chat.id,"Отлично! Ваш курс успешно изменен. Если вы ранее заполняли поля группа, пожалуйста, заполните её заново")
                json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
                user_info = json_work_new.get_info_about_unregistered_student(user_id)
                await bot.send_message( message.chat.id,user_info)

            
            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            user_markup.add('Изменить имя', 'Изменить фамилию')
            user_markup.add('Изменить факультет', 'Изменить курс')
            user_markup.add('Изменить группу')

            if dict_of_param["student_group"] != '':
                if json_work_new.group_has_headmen(dict_of_param["student_group"]) and dict_of_param['status'] == 'Студент 🤓':
                    user_markup.add("Назначить себя старостой 🤠")

            if dict_of_param["status"] == 'Староста 🤠':
                user_markup.add("Назначить себя студентом 🤓")

            if json_work_new.is_valid(dict_of_param):
                    user_markup.add('Завершить регистрацию')
            user_markup.add('Задать вопрос или сообщить об ошибке')
            user_markup.add('Отменить регистрацию')
            await bot.send_message( message.chat.id,reply_markup=user_markup)

        else:
            print("hello")
     
     
@dp.message_handler(lambda message: message.text == '1. Понедельник' or message.text == '2. Вторник' or message.text == '3. Среда' or message.text == '4. Четверг' or message.text == '5. Пятница' or message.text == '6. Суббота' or message.text == '7. Воскресенье')
async def cmd_start(message: types.Message): 
    user_id = str(message.chat.id)  
    user_status = json_work_new.get_user_status(user_id)

    if user_status == 'Староста 🤠' or user_status == 'Студент 🤓':
        day = message.text[0]
        timetable = json_work_new.get_timetable(user_id, user_weekday=int(day))
        bot.send_message(user_id, timetable)

        user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        
        if user_status == 'Студент 🤓':
            user_markup.add('Получить расписание')
            user_markup.add('Получить список студентов своей группы')

        else:
            user_markup.add('Получить расписание')
            user_markup.add('Получить список студентов своей группы')
            user_markup.add('Отправить сообщение своим студентам')
            user_markup.add('Отправить файл своим студентам')
            user_markup.add('Изменить расписание')

        user_markup.add('Задать вопрос или сообщить об ошибке')
        user_markup.add('Удалить профиль')
        await bot.send_message( message.chat.id,'Выберите пункт меню:', reply_markup=user_markup)
    
    else:
        json_work_new.update_last_user_command_t(user_id, "")
        await bot.send_message( message.chat.id,"Отказано в доступе")
    

@dp.message_handler(lambda message: message.text == 'Зарегистрироваться как преподаватель 👨‍🏫👩‍🏫')
async def cmd_start(message: types.Message): 
    user_id = str(message.chat.id)

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

            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

            user_markup.add('Изменить имя', 'Изменить фамилию')
            user_markup.add('Изменить отчество')
            user_markup.add('Задать вопрос или сообщить об ошибке')
            user_markup.add('Отменить регистрацию')

            json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
            info = json_work_new.get_info_about_unregistered_teacher(user_id)
            await bot.send_message( message.chat.id,info, reply_markup=user_markup)

        else:
            await bot.send_message( message.chat.id,"Вы уже начинали процесс регистрации")
            if json_work_new.get_user_status_un(user_id) == 'student':
                user_info = json_work_new.get_info_about_unregistered_student(user_id)
                dict_of_param = json_work_new.get_info_about_unregistered_student_dict(user_id)

                user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

                user_markup.add('Изменить имя', 'Изменить фамилию')
                user_markup.add('Изменить факультет', 'Изменить курс')
                user_markup.add('Изменить группу')

                if dict_of_param["student_group"] != '':
                    if json_work_new.group_has_headmen(dict_of_param["student_group"]) and dict_of_param['status'] == 'Студент 🤓':
                        user_markup.add("Назначить себя старостой 🤠")

                if dict_of_param["status"] == 'Староста 🤠':
                        user_markup.add("Назначить себя студентом 🤓")

                if json_work_new.is_valid(dict_of_param):
                    user_markup.add('Завершить регистрацию')
                user_markup.add('Задать вопрос или сообщить об ошибке')
                user_markup.add('Отменить регистрацию')

                await bot.send_message( message.chat.id,user_info, reply_markup=user_markup)

            else:
                user_info = json_work_new.get_info_about_unregistered_teacher(user_id)
                dict_of_param = json_work_new.get_info_about_unregistered_teacher_dict(user_id)

                user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

                user_markup.add('Изменить имя', 'Изменить фамилию')
                user_markup.add('Изменить отчество')
                if json_work_new.is_valid(dict_of_param):
                    user_markup.add('Завершить регистрацию')
                user_markup.add('Задать вопрос или сообщить об ошибке')
                user_markup.add('Отменить регистрацию')
                
                await bot.send_message( message.chat.id,user_info, reply_markup=user_markup)

    else:
        await bot.send_message( message.chat.id,"непонел")
        #Обнуление последних команд 
        
#513
@dp.message_handler(lambda message: "Изменить отчество" == message.text)
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id) 

    if not json_work_new.user_is_registered(user_id):
        if json_work_new.user_in_unregistered_list(user_id):
            if json_work_new.get_user_status_un(user_id) == 'teacher':
                json_work_new.update_last_user_command_un(user_id, message.text)

                user_markup = types.ReplyKeyboardMarkup(True, True)
                user_markup.add("Вернуться на главное меню")
                await bot.send_message( message.chat.id,"Введите отчество:", reply_markup=user_markup)

            else:
                json_work_new.update_last_user_command_un(user_id, "")
                user_markup = types.ReplyKeyboardMarkup(True, True)
                user_markup.add("Вернуться на главное меню")
                await bot.send_message( message.chat.id, "Вы что-то не понятное ввели", reply_markup=user_markup)

        else:
            await bot.send_message( message.chat.id, "Вы не зареганы в системе")

    else:
        #обнуление последних команд
        await bot.send_message( message.chat.id, "непонел")


@dp.message_handler(lambda message: "Зарегистрироваться как студент 🤓" == message.text)
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)

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

            user_markup = types.ReplyKeyboardMarkup(True, True)
            user_markup.add('Изменить имя', 'Изменить фамилию')
            user_markup.add('Изменить факультет', 'Изменить курс')
            user_markup.add('Изменить группу')
            user_markup.add('Задать вопрос или сообщить об ошибке')
            user_markup.add('Отменить регистрацию')
            json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
            info = json_work_new.get_info_about_unregistered_student(user_id)
            await bot.send_message( message.chat.id, info, reply_markup=user_markup)

        else:
            await bot.send_message( message.chat.id, "Вы начинали процесс регистрации")
            if json_work_new.get_user_status_un(user_id) == 'student':
                user_info = json_work_new.get_info_about_unregistered_student(user_id)
                dict_of_param = json_work_new.get_info_about_unregistered_student_dict(user_id)

                user_markup = types.ReplyKeyboardMarkup(True, True)

                user_markup.add('Изменить имя', 'Изменить фамилию')
                user_markup.add('Изменить факультет', 'Изменить курс')
                user_markup.add('Изменить группу')

                if dict_of_param["student_group"] != '':
                    if json_work_new.group_has_headmen(dict_of_param["student_group"]) and dict_of_param['status'] == 'Студент 🤓':
                        user_markup.add("Назначить себя старостой 🤠")

                if dict_of_param["status"] == 'Староста 🤠':
                        user_markup.add("Назначить себя студентом 🤓")

                if json_work_new.is_valid(dict_of_param):
                    user_markup.add('Завершить регистрацию')
                user_markup.add('Задать вопрос или сообщить об ошибке')
                user_markup.add('Отменить регистрацию')

                await bot.send_message( message.chat.id, user_info, reply_markup=user_markup)

            else:
                user_info = json_work_new.get_info_about_unregistered_teacher(user_id)
                dict_of_param = json_work_new.get_info_about_unregistered_teacher_dict(user_id)

                user_markup = types.ReplyKeyboardMarkup(True, True)

                user_markup.add('Изменить имя', 'Изменить фамилию')
                user_markup.add('Изменить отчество')
                if json_work_new.is_valid(dict_of_param):
                    user_markup.add('Завершить регистрацию')
                user_markup.add('Задать вопрос или сообщить об ошибке')
                user_markup.add('Отменить регистрацию')
                
                await bot.send_message( message.chat.id, user_info, reply_markup=user_markup)

    else:
        await bot.send_message( message.chat.id, "Не понел(")


#-----------------------------------------------------------------------

@dp.message_handler(lambda message: 'Завершить регистрацию' == message.text)
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)

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
                        await bot.send_message( message.chat.id, "Извините, но из вашей группы староста уже зарегистрированна в нашей системе")
                        dict_of_param['status'] = 'Студент 🤓'
                        json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
                        user_info = json_work_new.get_info_about_unregistered_student(user_id)

                        user_markup = types.ReplyKeyboardMarkup(True, True)

                        user_markup.add('Изменить имя', 'Изменить фамилию')
                        user_markup.add('Изменить факультет', 'Изменить курс')
                        user_markup.add('Изменить группу')

                        if dict_of_param["student_group"] != '':
                            if json_work_new.group_has_headmen(dict_of_param["student_group"]) and dict_of_param['status'] == 'Студент 🤓':
                                user_markup.add("Назначить себя старостой 🤠")

                        if dict_of_param["status"] == 'Староста 🤠':
                            user_markup.add("Назначить себя студентом 🤓")

                        if json_work_new.is_valid(dict_of_param):
                            user_markup.add('Завершить регистрацию')
                        user_markup.add('Задать вопрос или сообщить об ошибке')
                        user_markup.add('Отменить регистрацию')

                        await bot.send_message( message.chat.id, user_info, reply_markup=user_markup)
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

                    await bot.send_message( message.chat.id, text)
                    await bot.send_message( message.chat.id, "Спасибо, что начали пользоваться нашим ботом☺️\nКоманда разработчиков надееться, что у вас будет положительный опыт использования нашего бота")
                    await bot.send_message( message.chat.id, "В знак благодарности мы даем тебе наши фирменные стикеры, которое ты можешь использовать как для коммуникации с ботом, так и для своих нужд")
                    await bot.send_message( message.chat.id, "CAACAgIAAxkBAAMCX5sLPFCziNQRdIwrp9crs6n4yB4AAmwJAAKzkqlINHYOQQw5FBIbBA")
                    if dict_of_param["name_of_faculty"] == "Хакатон":
                        await bot.send_message( message.chat.id, "Для напоминания о проходящем хакатоне, мы также сделали специальный стикерпак для всех его участников.")
                        await bot.send_message( message.chat.id, "CAACAgIAAxkBAAM4X55fZiWhZrxKcOkufF0L5dHxG38AAqwNAAJhW7hInjwCajgPoKseBA")
                    
                    user_markup = types.ReplyKeyboardMarkup(True, True)
                    user_markup.add("/help")
                    await bot.send_message( message.chat.id, "Введите команду /help для получения доступных команд", reply_markup=user_markup)
                else:
                    dict_of_param["chosen_faculty"] = ""
                    dict_of_param["teacher_msg"] = ""
                    json_work_new.remove_unregistered_user(user_id)
                    text = json_work_new.add_new_teacher(dict_of_param, user_id)

                    await bot.send_message( message.chat.id, text)
                    await bot.send_message( message.chat.id, "Спасибо, что начали пользоваться нашим ботом☺️\nКоманда разработчиков надееться, что у вас будет положительный опыт использования нашего бота")
                    await bot.send_message( message.chat.id, "В знак благодарности мы даем тебе наши фирменные стикеры, которое ты можешь использовать как для коммуникации с ботом, так и для своих нужд")
                    
                    
                    #---------------------------------------------------------------------------------
                    
                    
                    
                    bot.send_sticker(message.from_user.id, "CAACAgIAAxkBAAMCX5sLPFCziNQRdIwrp9crs6n4yB4AAmwJAAKzkqlINHYOQQw5FBIbBA")
                    
                    user_markup = types.ReplyKeyboardMarkup(True, False)
                    user_markup.add("/help")
                    await bot.send_message( message.chat.id, "Введите команду /help для получения доступных команд", reply_markup=user_markup)


@dp.message_handler(lambda message: "Удалить профиль" == message.text )
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)

    if json_work_new.user_is_registered(user_id):
        user_markup = types.ReplyKeyboardMarkup(True, False)
        user_markup.add("Да, я хочу удалить свой профиль")
        user_markup.add("Нет, я просто так нажал эту кнопку🙃")
        await bot.send_message( message.chat.id, "Вы точно хотите удалить свой профиль?", reply_markup=user_markup)

@dp.message_handler(lambda message: "Да, я хочу удалить свой профиль" == message.text )
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)

    if json_work_new.user_is_registered(user_id):
        user_status = json_work_new.get_user_status(user_id)

        '''if user_status == 'Учитель 👨‍🏫👩‍🏫':
            json_work_new.remove_teacher(user_id)
        else:
            json_work_new.remove_student(user_id)'''
        
        user_markup = types.ReplyKeyboardMarkup(True, True)
        user_markup.add("Да, я хочу написать про свой опыт")
        user_markup.add('Нет, я не хочу написать про свой опыт')
        user_markup.add('Отменить действие')
        await bot.send_message( message.chat.id, "Может вы хотите написать нам про ваш опыт использования бота?\nЭто поможет нам в улучшении качества нашего продукта", reply_markup=user_markup)


@dp.message_handler(lambda message: "Да, я хочу написать про свой опыт" == message.text )
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)
    if json_work_new.user_is_registered(user_id):
        user_status = json_work_new.get_user_status(user_id)

        if user_status == 'Учитель 👨‍🏫👩‍🏫':
            json_work_new.update_last_user_command_t(user_id, "Оставить отзыв")
        else:
            json_work_new.update_last_user_command_s(user_id, "Оставить отзыв")
        
        user_markup = types.ReplyKeyboardMarkup(True, True)
        user_markup.add('Отменить действие')
        await bot.send_message( message.chat.id, "Введите сообщение", reply_markup=user_markup)



@dp.message_handler(lambda message: "Нет, я не хочу написать про свой опыт" == message.text )
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)
    if json_work_new.user_is_registered(user_id):
        user_status = json_work_new.get_user_status(user_id)

        if user_status == 'Учитель 👨‍🏫👩‍🏫':
            json_work_new.remove_teacher(user_id)
        else:
            json_work_new.remove_student(user_id)
        
        user_markup = types.ReplyKeyboardMarkup(True, True)
        user_markup.add("/start")
        await bot.send_message( message.chat.id, "Ваш профиль удален😥")
        await bot.send_message( message.chat.id, "Напишите /start для регистрации", reply_markup=user_markup)

        

@dp.message_handler(lambda message: "Нет, я просто так нажал эту кнопку🙃" == message.text )
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)

    if json_work_new.user_is_registered(user_id):
        user_markup = types.ReplyKeyboardMarkup(True, True)
        user_markup.add("/help")
        await bot.send_message( message.chat.id, "Вот и отлично) Напишите /help для получения списка доступных команд", reply_markup=user_markup)


@dp.message_handler(lambda message: 'Назначить себя старостой 🤠' == message.text )
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)

    if not json_work_new.user_is_registered(user_id):

        if json_work_new.user_in_unregistered_list(user_id):
            if json_work_new.get_user_status_un(user_id) == 'student':

                dict_of_param = json_work_new.get_info_about_unregistered_student_dict(user_id)
                dict_of_param['status'] = "Староста 🤠"

                json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
                user_info = json_work_new.get_info_about_unregistered_student(user_id)

                user_markup = types.ReplyKeyboardMarkup(True, True)

                user_markup.add('Изменить имя', 'Изменить фамилию')
                user_markup.add('Изменить факультет', 'Изменить курс')
                user_markup.add('Изменить группу')

                if dict_of_param["student_group"] != '':
                    if json_work_new.group_has_headmen(dict_of_param["student_group"]) and dict_of_param['status'] == 'Студент 🤓':
                        user_markup.add("Назначить себя старостой 🤠")

                if dict_of_param["status"] == 'Староста 🤠':
                        user_markup.add("Назначить себя студентом 🤓")

                if json_work_new.is_valid(dict_of_param):
                    user_markup.add('Завершить регистрацию')
                user_markup.add('Задать вопрос или сообщить об ошибке')
                user_markup.add('Отменить регистрацию')

                await bot.send_message( message.chat.id, user_info, reply_markup=user_markup)


@dp.message_handler(lambda message: 'Назначить себя студентом 🤓' == message.text )
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)

    if not json_work_new.user_is_registered(user_id):

        if json_work_new.user_in_unregistered_list(user_id):
            if json_work_new.get_user_status_un(user_id) == 'student':

                dict_of_param = json_work_new.get_info_about_unregistered_student_dict(user_id)
                dict_of_param['status'] = "Студент 🤓"

                json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
                user_info = json_work_new.get_info_about_unregistered_student(user_id)

                user_markup = types.ReplyKeyboardMarkup(True, True)

                user_markup.add('Изменить имя', 'Изменить фамилию')
                user_markup.add('Изменить факультет', 'Изменить курс')
                user_markup.add('Изменить группу')

                if dict_of_param["student_group"] != '':
                    if json_work_new.group_has_headmen(dict_of_param["student_group"]) and dict_of_param['status'] == 'Студент 🤓':
                        user_markup.add("Назначить себя старостой 🤠")

                if dict_of_param["status"] == 'Староста 🤠':
                        user_markup.add("Назначить себя студентом 🤓")

                if json_work_new.is_valid(dict_of_param):
                    user_markup.add('Завершить регистрацию')
                user_markup.add('Задать вопрос или сообщить об ошибке')
                user_markup.add('Отменить регистрацию')

                await bot.send_message( message.chat.id, user_info, reply_markup=user_markup)



@dp.message_handler(lambda message: 'Вернуться на главное меню' == message.text )
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)

    if not json_work_new.user_is_registered(user_id):

        if json_work_new.user_in_unregistered_list(user_id):
            if json_work_new.get_user_status_un(user_id) == 'student':
                user_info = json_work_new.get_info_about_unregistered_student(user_id)
                dict_of_param = json_work_new.get_info_about_unregistered_student_dict(user_id)

                user_markup = types.ReplyKeyboardMarkup(True, True)

                user_markup.add('Изменить имя', 'Изменить фамилию')
                user_markup.add('Изменить факультет', 'Изменить курс')
                user_markup.add('Изменить группу')

                if dict_of_param["student_group"] != '':
                    if json_work_new.group_has_headmen(dict_of_param["student_group"]) and dict_of_param['status'] == 'Студент 🤓':
                        user_markup.add("Назначить себя старостой 🤠")

                if dict_of_param["status"] == 'Староста 🤠':
                        user_markup.add("Назначить себя студентом 🤓")

                if json_work_new.is_valid(dict_of_param):
                    user_markup.add('Завершить регистрацию')
                user_markup.add('Задать вопрос или сообщить об ошибке')
                user_markup.add('Отменить регистрацию')

                await bot.send_message( message.chat.id, user_info, reply_markup=user_markup)

            else:
                user_info = json_work_new.get_info_about_unregistered_teacher(user_id)
                dict_of_param = json_work_new.get_info_about_unregistered_teacher_dict(user_id)

                user_markup = types.ReplyKeyboardMarkup(True, True)

                user_markup.add('Изменить имя', 'Изменить фамилию')
                user_markup.add('Изменить отчество')
                if json_work_new.is_valid(dict_of_param):
                    user_markup.add('Завершить регистрацию')
                user_markup.add('Задать вопрос или сообщить об ошибке')
                user_markup.add('Отменить регистрацию')
                
                await bot.send_message( message.chat.id, user_info, reply_markup=user_markup)

    else:
        '''Обнуление последней команды и сообщения бота в зависимости от статуса'''
        await bot.send_message( message.chat.id, "не понел")

        
@dp.message_handler(lambda message: 'Изменить имя' == message.text )
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)

    if not json_work_new.user_is_registered(user_id):
        if json_work_new.user_in_unregistered_list(user_id):
        
            json_work_new.update_last_user_command_un(user_id, message.text)

            user_markup = types.ReplyKeyboardMarkup(True, True)
            user_markup.add("Вернуться на главное меню")
            await bot.send_message( message.chat.id, "Введите имя:", reply_markup=user_markup)

        else:
            await bot.send_message( message.chat.id, 'Вы ещё не начинали процесс регистрации')
            #го регаться

    else:
        #обнуление команд
        await bot.send_message( message.chat.id, "непонел")
        
@dp.message_handler(lambda message: "Изменить фамилию" == message.text )
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)
    
    if not json_work_new.user_is_registered(user_id):
        if json_work_new.user_in_unregistered_list(user_id):
        
            json_work_new.update_last_user_command_un(user_id, message.text)

            user_markup = types.ReplyKeyboardMarkup(True, True)
            user_markup.add("Вернуться на главное меню")
            await bot.send_message( message.chat.id, "Введите фамилию:", reply_markup=user_markup)

        else:
            await bot.send_message( message.chat.id, 'Вы ещё не начинали процесс регистрации')
            user_markup = types.ReplyKeyboardMarkup(True, True)
            user_markup.add('Зарегистрироваться как студент 🤓')
            user_markup.add('Зарегистрироваться как преподаватель 👨‍🏫👩‍🏫')
            await bot.send_message( message.chat.id, "Давай попробуем зарегистрироваться☺️", reply_markup=user_markup)

    else:
        #обнуление команд
        await bot.send_message( message.chat.id, "непонел")   
         
@dp.message_handler(lambda message: "Изменить факультет" == message.text )
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)

    if json_work_new.user_in_unregistered_list(user_id):
        json_work_new.update_last_user_command_un(user_id, message.text)
        
        faculties = json_work_new.get_list_of_faculties()
        user_markup = types.ReplyKeyboardMarkup(True, True)
        for faculty in faculties:
            user_markup.add(faculty)

        user_markup.add("Вернуться на главное меню")
        await bot.send_message( message.chat.id, 'Выберите факультет:', reply_markup=user_markup)

    elif json_work_new.user_is_registered(telegram_id):
        await bot.send_message( message.chat.id, 'Вы уже зарегистрированы')         

@dp.message_handler(lambda message: 'Изменить курс'== message.text )
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)

    if json_work_new.user_in_unregistered_list(user_id):
        
        json_work_new.update_last_user_command_un(user_id, message.text)
        user_markup = types.ReplyKeyboardMarkup(True, True)

        for course_num in range (1, 7, 2):
            course = str(course_num) + ' курс'
            course_p = str(course_num + 1) + ' курс'
            user_markup.add(course, course_p)

        user_markup.add("Вернуться на главное меню")
        await bot.send_message( message.chat.id, 'Выберите курс:', reply_markup=user_markup)
        
    elif json_work_new.user_is_registered(telegram_id):
        await bot.send_message( message.chat.id, 'Вы уже зарегистрированы')     
        

@dp.message_handler(lambda message: 'Изменить группу'== message.text )
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)
    if json_work_new.user_in_unregistered_list(user_id):
        dict_of_param = json_work_new.get_info_about_unregistered_student_dict(user_id)
        if dict_of_param['year_of_study'] != '':
            json_work_new.update_last_user_command_un(user_id, message.text)
            groups = json_work_new.get_list_of_group(dict_of_param["name_of_faculty"], dict_of_param["year_of_study"])[1]
            user_markup = types.ReplyKeyboardMarkup(True, True)
            for group in groups:
                user_markup.add(group)
            user_markup.add("Вернуться на главное меню")
            await bot.send_message( message.chat.id, 'Выберите группу:', reply_markup=user_markup)
        else:
            await bot.send_message( message.chat.id, "Сначала заполните поля факультета и курса!😡")

            user_info = json_work_new.get_info_about_unregistered_student(user_id)
            dict_of_param = json_work_new.get_info_about_unregistered_student_dict(user_id)

            user_markup = types.ReplyKeyboardMarkup(True, True)

            user_markup.add('Изменить имя', 'Изменить фамилию')
            user_markup.add('Изменить факультет', 'Изменить курс')
            user_markup.add('Изменить группу')
            if dict_of_param["student_group"] != '':
                if json_work_new.group_has_headmen(dict_of_param["student_group"]) and dict_of_param['status'] == 'Студент 🤓':
                    user_markup.add("Назначить себя старостой 🤠")

            if dict_of_param["status"] == 'Староста 🤠':
                        user_markup.add("Назначить себя студентом 🤓")

            if json_work_new.is_valid(dict_of_param):
                user_markup.add('Завершить регистрацию')
            user_markup.add('Задать вопрос или сообщить об ошибке')
            user_markup.add('Отменить регистрацию')

            await bot.send_message( message.chat.id, user_info, reply_markup=user_markup)
    elif json_work_new.user_is_registered(telegram_id):
        await bot.send_message( message.chat.id, 'Вы уже зарегистрированы')          
     













#1020
@dp.message_handler(lambda message: message.text == 'Отменить регистрацию')
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)

    if not json_work_new.user_is_registered(user_id):
        if json_work_new.user_in_unregistered_list(user_id):
            json_work_new.remove_unregistered_user(user_id)
            await bot.send_message( message.chat.id,"Регистрация отменена😥")

            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            user_markup.add('Зарегистрироваться как студент 🤓')
            user_markup.add('Зарегистрироваться как преподаватель 👨‍🏫👩‍🏫')
            await bot.send_message( message.chat.id,"Давай опять попробуем зарегистрироваться☺️", reply_markup=user_markup)
        else:
            await bot.send_message( message.chat.id,"Да вы вроде и не регались...")

            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            user_markup.add('Зарегистрироваться как студент 🤓')
            user_markup.add('Зарегистрироваться как преподаватель 👨‍🏫👩‍🏫')
            await bot.send_message( message.chat.id,"Давай попробуем зарегистрироваться☺️", reply_markup=user_markup)

    else:
        '''Обнуление последних команд'''
        await bot.send_message( message.chat.id,"непонел")
        
        
@dp.message_handler(lambda message: message.text == "Изменить расписание")
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)
    if json_work_new.user_is_registered(user_id):
        user_status = json_work_new.get_user_status(user_id)
        if user_status == 'Староста 🤠':
            headmen_info = json_work_new.get_info_about_student_dict(user_id)
            token = list(random.choice(string.ascii_lowercase) for i in range(10))
            token[0] = 'u'
            token[4] = 'n'
            token[7] = 'i'
            keyboard = types.InlineKeyboardMarkup()
            url_button = types.InlineKeyboardButton(text="Ссылка на сайт", url=f"https://yabzik.online/unisystem/public/schedule/{headmen_info['code_of_group']}-d/{headmen_info['year_of_study']}?token={''.join(token)}")
            keyboard.add(url_button)
            await bot.send_message( message.chat.id,"Изменить расписание вы можете на нашем сайте по ссылке ниже.", reply_markup=keyboard)
            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            user_markup.add('Получить расписание')
            user_markup.add('Получить список студентов своей группы')
            user_markup.add('Отправить сообщение своим студентам')
            user_markup.add('Отправить файл своим студентам')
            user_markup.add('Изменить расписание')
            user_markup.add('Задать вопрос или сообщить об ошибке')
            user_markup.add('Удалить профиль')
            await bot.send_message( message.chat.id,'Выберите пункт меню:', reply_markup=user_markup)
            
            
@dp.message_handler(lambda message: message.text == "Отправить файл своим студентам")
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)
    user_status = json_work_new.get_user_status(user_id)

    if user_status == 'Староста 🤠' :
        #if last_command == 
        json_work_new.update_last_user_command_s(user_id, message.text)
        json_work_new.update_last_bot_msg_s(user_id, 'Введите сообщение:')
        user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        user_markup.add('Отменить действие')
        await bot.send_message( message.chat.id,'Введите сообщение:', reply_markup=user_markup)

    else:
        if status == 'Студент 🤓':
            json_work_new.update_last_user_command_s(user_id, "")

        elif status == 'Учитель 👨‍🏫👩‍🏫':
            json_work_new.update_last_user_command_t(user_id, "")
        await bot.send_message( message.chat.id,"Отказано в доступе")
        
        
@dp.message_handler()
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)

    if json_work_new.user_is_registered(user_id):
        print('hello')
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
            await bot.send_message(message.chat.id, group_list) 
            json_work_new.update_chosen_faculty(user_id, student_group)
            json_work_new.update_last_user_command_t(user_id, "")
            json_work_new.update_last_bot_msg_t(user_id, "")
            
            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            user_markup.add('Получить список студентов')
            user_markup.add('Отправить сообщение студентам')
            user_markup.add('Отправить файл студентам')

            
            json_work_new.update_chosen_faculty(user_id, "")

            user_markup.add('Задать вопрос или сообщить об ошибке')
            user_markup.add('Удалить профиль')
            await bot.send_message( message.chat.id,'Выберите действие:', reply_markup=user_markup)

        elif user_status == 'Учитель 👨‍🏫👩‍🏫' and user_command == 'Отправить сообщение студентам' and bot_command == 'Выберите название группы, сутдентам которой вы хотите отправить сообщение':
            student_group = message.text
            json_work_new.update_chosen_faculty(user_id, student_group)
            group_list_id = json_work_new.get_group_list_id(student_group)

            if len(group_list_id):
                json_work_new.update_last_bot_msg_t(user_id, "Введите сообщение:")
                user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                user_markup.add('Отменить действие')
                await bot.send_message( message.chat.id,'Введите сообщение:', reply_markup=user_markup)
                


            else:
                await bot.send_message(message.chat.id, f"Пока нет зарегистрированных студентов в нашей системе из группы {student_group} 😐")

                user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                user_markup.add('Получить список студентов')
                user_markup.add('Отправить сообщение студентам')
                user_markup.add('Отправить файл студентам')
                user_markup.add('Задать вопрос или сообщить об ошибке')
                user_markup.add('Удалить профиль')
                await bot.send_message( message.chat.id,'Выберите пункт меню:', reply_markup=user_markup)
                json_work_new.update_last_user_command_t(user_id, "")
                json_work_new.update_last_bot_msg_t(user_id, "")
                json_work_new.update_chosen_faculty(user_id, "")

        elif user_status == 'Учитель 👨‍🏫👩‍🏫' and user_command == 'Отправить сообщение студентам' and bot_command == 'Введите сообщение:':            
            teacher_msg = message.text

            student_group = json_work_new.get_chosen_faculty(user_id)
            group_list_id = json_work_new.get_group_list_id(student_group)
            answer = json_work_new.get_answer_t(user_id)
            

            for student_id in group_list_id:
                teacher_initials = json_work_new.get_teacher_name_and_father_name(str(message.chat.id))
                teachers_msg ='Преподаватель ' + teacher_initials + ' отправил сообщение студентам вашей группы:\n' + message.text
                print(answer)
                if answer != "Нет, студенты не смогут ответить":
                    print('ffffffffrg;pehkeo[thkttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt')
                    if answer == 'Оставить эту возможность только старосте' or answer == "Да, студенты смогут ответить": and json_work_new.user_is_headmen(str(student_id)):
                    #if answer == "Да, студенты смогут ответить":
                        keyboard = types.InlineKeyboardMarkup()
                        callback_button = types.InlineKeyboardButton(text="Ответить на сообщение", callback_data=user_id + ' ' + str(message.message_id))
                        keyboard.add(callback_button)
                        callback_button = types.InlineKeyboardButton(text="Отправить файл", callback_data='Ф' + user_id + ' ' + str(message.message_id))
                        keyboard.add(callback_button)
                        callback_button = types.InlineKeyboardButton(text="Не отвечать на сообщение", callback_data="nothing")
                        keyboard.add(callback_button)
                        await bot.send_message(student_id, teachers_msg, reply_markup=keyboard)
                    await bot.send_message(student_id, teachers_msg)
                     #   print('ffffffffrg;prgegrggggggggggegftttttttttttttttttttttttttttttttttttttttttttttttttttttt')
                    else:
                        await bot.send_message(student_id, teachers_msg)
                else:
                    await bot.send_message( message.chat.id,student_id, teachers_msg)
                    #print('frogkerp[hj[pobjp')
                    await bot.send_message(student_id, teachers_msg)


            await bot.send_message( message.chat.id,f"Ваше сообщение успешно доставлено студентам группы {student_group}!")
            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            user_markup.add('Получить список студентов')
            user_markup.add('Отправить сообщение студентам')
            user_markup.add('Отправить файл студентам')
            user_markup.add('Задать вопрос или сообщить об ошибке')
            user_markup.add('Удалить профиль')
            await bot.send_message( message.chat.id,'Выберите пункт меню:', reply_markup=user_markup)
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
                keyboard = types.InlineKeyboardMarkup()
                callback_button = types.InlineKeyboardButton(text="Ответить на сообщение", callback_data=user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = types.InlineKeyboardButton(text="Отправить файл", callback_data='Ф' + user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = types.InlineKeyboardButton(text="Не отвечать на сообщение", callback_data="nothing")
                keyboard.add(callback_button)
                await bot.send_message(int(teacher_id_info[0]), text, reply_markup=keyboard, reply_to_message_id=int(teacher_id_info[3]))
                await bot.send_message(message.chat.id,"Ваше сообщение успешно доставлено преподавателю!")
            else:
                await bot.send_message(message.chat.id,"Преподаватель уже удален из базы😥")

            await bot.edit_message_text(chat_id=message.chat.id, message_id=int(teacher_id_info[1]), text=teacher_id_info[2])

            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            user_markup.add('Получить расписание')
            if user_status == 'Староста 🤠':
                user_markup.add('Получить список студентов своей группы')
                user_markup.add('Отправить сообщение своим студентам')
                user_markup.add('Отправить файл своим студентам')
                user_markup.add('Изменить расписание')
            else:
                user_markup.add('Получить список студентов своей группы')
            user_markup.add('Задать вопрос или сообщить об ошибке')
            user_markup.add('Удалить профиль')
            await bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=user_markup)
            json_work_new.update_last_user_command_s(user_id, "")
            json_work_new.update_last_bot_msg_s(user_id, "")
            json_work_new.update_last_user_id_s(user_id, [])


        elif user_status == 'Учитель 👨‍🏫👩‍🏫' and user_command == "Ответить на сообщение":
            

            teacher_initials = json_work_new.get_teacher_name_and_father_name(str(message.chat.id))
            teacher_msg = 'Преподаватель ' + teacher_initials + ' ответил на ваше сообщение:\n' + message.text
            student_id_info = json_work_new.get_last_user_id_t(user_id)

            if json_work_new.user_is_registered(student_id_info[0]):            
                keyboard = types.InlineKeyboardMarkup()
                callback_button = types.InlineKeyboardButton(text="Ответить на сообщение", callback_data=user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = types.InlineKeyboardButton(text="Отправить файл", callback_data='Ф' + user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = types.InlineKeyboardButton(text="Не отвечать на сообщение", callback_data="nothing")
                keyboard.add(callback_button)
                await bot.send_message(int(student_id_info[0]), teacher_msg, reply_markup=keyboard, reply_to_message_id=int(student_id_info[3]))
                await bot.send_message(message.chat.id, "Ваше сообщение успешно доставлено студенту!")
            else:
                bot.send_message(message.chat.id, "Студент уже удален из базы😥")
            await bot.edit_message_text(chat_id=message.chat.id, message_id=int(student_id_info[1]), text=student_id_info[2])

            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            user_markup.add('Получить список студентов')
            user_markup.add('Отправить сообщение студентам')
            user_markup.add('Отправить файл студентам')
            user_markup.add('Задать вопрос или сообщить об ошибке')
            user_markup.add('Удалить профиль')

            await bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=user_markup)
            json_work_new.update_last_user_command_t(user_id, "")
            json_work_new.update_last_bot_msg_t(user_id, "")
            json_work_new.update_last_user_id_t(user_id, [])

        elif user_status == 'Староста 🤠' and user_command == "Ответить на сообщение студента":
            headmen_info = json_work_new.get_info_about_student_dict(user_id)
            student_id_info = json_work_new.get_last_user_id_s(user_id)
            if json_work_new.user_is_registered(student_id_info[0]):
                headmen_msg = 'Староста из вашей группы ответил на ваше сообщение:\n' + message.text
            
                keyboard = types.InlineKeyboardMarkup()
                callback_button = types.InlineKeyboardButton(text="Ответить на сообщение", callback_data='С' + user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = types.InlineKeyboardButton(text="Отправить файл", callback_data='ФС' + user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = types.InlineKeyboardButton(text="Не отвечать на сообщение", callback_data="nothing")
                keyboard.add(callback_button)
                await bot.send_message(int(student_id_info[0]), headmen_msg, reply_markup=keyboard, reply_to_message_id=int(student_id_info[3]))
                await bot.send_message(message.chat.id, "Ваше сообщение успешно доставлено студенту!")
            else:
                await bot.send_message(message.chat.id, "Студент уже удален из базы😥")

            await bot.edit_message_text(chat_id=message.chat.id, message_id=int(student_id_info[1]), text=student_id_info[2])

            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            user_markup.add('Получить расписание')
            user_markup.add('Получить список студентов своей группы')
            user_markup.add('Отправить сообщение своим студентам')
            user_markup.add('Отправить файл своим студентам')
            user_markup.add('Изменить расписание')
            user_markup.add('Задать вопрос или сообщить об ошибке')
            user_markup.add('Удалить профиль')

            await bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=user_markup)
            json_work_new.update_last_user_command_s(user_id, "")
            json_work_new.update_last_bot_msg_s(user_id, "")
            json_work_new.update_last_user_id_s(user_id, [])



        elif user_status == 'Староста 🤠' and user_command == 'Отправить сообщение своим студентам':
            headman_group = json_work_new.get_student_group(user_id)
            group_list_id = json_work_new.get_group_list_id_for_headmen(headman_group)
            headman_text_for_students = "Староста вашей группы отправил сообщение студентам:\n" + message.text

            if len(group_list_id):

                for student_id in group_list_id:
                    keyboard = types.InlineKeyboardMarkup()
                    callback_button = types.InlineKeyboardButton(text="Ответить на сообщение", callback_data='С' + user_id + ' ' + str(message.message_id))
                    keyboard.add(callback_button)
                    callback_button = types.InlineKeyboardButton(text="Отправить файл", callback_data='ФС' + user_id + ' ' + str(message.message_id))
                    keyboard.add(callback_button)
                    callback_button = types.InlineKeyboardButton(text="Не отвечать на сообщение", callback_data="nothing")
                    keyboard.add(callback_button)
                    bot.send_message(student_id, headman_text_for_students, reply_markup=keyboard)
                
                await bot.send_message(message.chat.id, "Ваше сообщение успешно доставлено студентам вашей группы!")
            else:
                await bot.send_message(message.chat.id, "В нашей базе студентов из вашей группы ещё нет(")

            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            user_markup.add('Получить расписание')
            user_markup.add('Получить список студентов своей группы')
            user_markup.add('Отправить сообщение своим студентам')
            user_markup.add('Отправить файл своим студентам')
            user_markup.add('Изменить расписание')
            user_markup.add('Задать вопрос или сообщить об ошибке')
            user_markup.add('Удалить профиль')
            await bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=user_markup)

        elif user_status == 'Студент 🤓' and user_command == 'Ответить на сообщение старосты':
            student_info = json_work_new.get_info_about_student_dict(user_id)
            headmen_id_info = json_work_new.get_last_user_id_s(user_id)
            if json_work_new.user_is_registered(headmen_id_info[0]):
                student_msg = f'Студент из вашей группы, {student_info["student_family_name"]} {student_info["student_name"]} ответил на ваше сообщение:\n' + message.text
            
                keyboard = types.InlineKeyboardMarkup()
                callback_button = types.InlineKeyboardButton(text="Ответить на сообщение", callback_data='С' + user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = types.InlineKeyboardButton(text="Отправить файл", callback_data='ФС' + user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = types.InlineKeyboardButton(text="Не отвечать на сообщение", callback_data="nothing")
                keyboard.add(callback_button)
                await bot.send_message(int(headmen_id_info[0]), student_msg, reply_markup=keyboard, reply_to_message_id=int(headmen_id_info[3]))
                await bot.send_message(message.chat.id, "Ваше сообщение успешно доставлено старосте!")
            else:
                await bot.send_message(message.chat.id, "Староста уже удален из базы😥")

            await bot.edit_message_text(chat_id=message.chat.id, message_id=int(headmen_id_info[1]), text=headmen_id_info[2])

            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            user_markup.add('Получить список студентов')
            user_markup.add('Получить список студентов своей группы')
            user_markup.add('Задать вопрос или сообщить об ошибке')
            user_markup.add('Удалить профиль')

            await bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=user_markup)
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
                user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                user_markup.add('Отменить действие')
                await bot.send_message(message.chat.id, 'Введите сообщение:', reply_markup=user_markup)
                


            else:
                await bot.send_message(message.chat.id, f"Пока нет зарегистрированных студентов в нашей системе из группы {student_group} 😐")

                user_markup = types.ReplyKeyboardMarkup(True, False)
                user_markup.add('Получить список студентов')
                user_markup.add('Отправить сообщение студентам')
                user_markup.add('Отправить файл студентам')
                user_markup.add('Задать вопрос или сообщить об ошибке')
                user_markup.add('Удалить профиль')
                await bot.send_message(message.chat.id, 'Выберите пункт меню:', reply_markup=user_markup)
                json_work_new.update_last_user_command_t(user_id, "")
                json_work_new.update_last_bot_msg_t(user_id, "")
                json_work_new.update_chosen_faculty(user_id, "")

        elif user_status == 'Учитель 👨‍🏫👩‍🏫' and user_command == 'Отправить файл студентам' and bot_command == 'Введите сообщение:':
            json_work_new.update_teacher_msg(user_id, message.text)

            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            user_markup.add('Отменить действие')
            await bot.send_message(message.chat.id, 'Загрузите файл (он должен быть не больше 50 Мб!)', reply_markup=user_markup)

        elif user_status != 'Учитель 👨‍🏫👩‍🏫' and bot_command == 'Введите сообщение, которое прийдет вместе с вашим файлом:':
            json_work_new.update_student_msg(user_id, message.text)

            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            user_markup.add('Отменить действие')
            await bot.send_message(message.chat.id, 'Загрузите файл (он должен быть не больше 50 Мб!)', reply_markup=user_markup)

        elif user_status == 'Учитель 👨‍🏫👩‍🏫' and bot_command == 'Введите сообщение, которое прийдет вместе с вашим файлом:':
            json_work_new.update_teacher_msg(user_id, message.text)

            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            user_markup.add('Отменить действие')
            await bot.send_message(message.chat.id, 'Загрузите файл (он должен быть не больше 50 Мб!)', reply_markup=user_markup)



        elif user_status == 'Староста 🤠' and user_command == 'Отправить файл своим студентам' and bot_command == 'Введите сообщение:':
            json_work_new.update_student_msg(user_id, message.text)

            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            user_markup.add('Отменить действие')
            await bot.send_message(message.chat.id, 'Загрузите файл (он должен быть не больше 50 Мб!)', reply_markup=user_markup)

        elif user_status == 'Староста 🤠' and user_command == 'Отправить файл студенту' or user_status == 'Студент 🤓' and user_command == 'Отправить файл старосте':
            json_work_new.update_student_msg(user_id, message.text)

            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            user_markup.add('Отменить действие')
            await bot.send_message(message.chat.id, 'Загрузите файл (он должен быть не больше 50 Мб!)', reply_markup=user_markup)

        elif user_command == 'Задать вопрос или сообщить об ошибке':
            user_msg = f'Пользователь задал вам вопрос или сообщил об ошибке:\n {message.text}'
            for dev_id in ["1254134824", "507634108", "215080778"]:
                if json_work_new.user_is_registered(dev_id):
                    keyboard = types.InlineKeyboardMarkup()
                    callback_button = types.InlineKeyboardButton(text="Ответить на сообщение", callback_data='Р' + user_id + ' ' + str(message.message_id))
                    keyboard.add(callback_button)
                    bot.send_message(int(dev_id), user_msg, reply_markup=keyboard)
            await bot.send_message(message.chat.id, "Ваше сообщение доставлено разработчикам! Они постараются вам в ближайшее время ответить")
            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            user_markup.add("/help")
            await bot.send_message(message.chat.id, "Введите /help для получения списка команд", reply_markup=user_markup)
            if user_status != 'Учитель 👨‍🏫👩‍🏫':
                json_work_new.update_last_user_command_s(user_id, "")
            else:
                json_work_new.update_last_user_command_t(user_id, "")

        elif user_command == 'Ответить на сообщение пользователя':
            if user_status != 'Учитель 👨‍🏫👩‍🏫':
                dev_name = json_work_new.get_info_about_student_dict(user_id)["student_name"]
                user_id_info = json_work_new.get_last_user_id_s(user_id)
            else:
                dev_name = teacher_initials = json_work_new.get_teacher_name_and_father_name(str(message.chat.id)).split()[1]
                user_id_info = json_work_new.get_last_user_id_t(user_id)

            
            dev_msg = f'Разработчик {dev_name} ответил на ваше сообщение:\n' + message.text
            await bot.send_message(int(user_id_info[0]), dev_msg, reply_to_message_id=int(user_id_info[3]))
            await bot.send_message(message.chat.id, "Ваше сообщение успешно доставлено пользователю!")

            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            user_markup.add('/help')

            await bot.send_message(message.chat.id, 'Напишите /help для получения списка доступных команд', reply_markup=user_markup)
            if user_status != 'Учитель 👨‍🏫👩‍🏫':
                json_work_new.update_last_user_command_s(user_id, "")
            else:
                json_work_new.update_last_user_command_t(user_id, "")

        elif user_command == 'Оставить отзыв':
            user_msg = f'Пользователь описал опыт использования ботом:\n{message.text}'
            for dev_id in ["1254134824", "507634108", "215080778"]:
                if json_work_new.user_is_registered(dev_id):
                    bot.send_message(int(dev_id), user_msg)
            await bot.send_message(message.chat.id, "Ваше сообщение доставлено разработчикам! Спасибо, что описали свой опыт использования нашим ботом")

            if user_status == 'Учитель 👨‍🏫👩‍🏫':
                json_work_new.remove_teacher(user_id)
            else:
                json_work_new.remove_student(user_id)
        
            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            user_markup.add("/start")
            await bot.send_message(message.chat.id, "Ваш профиль удален😥")
            await bot.send_message(message.chat.id, "Напишите /start для регистрации", reply_markup=user_markup)




        else:
            await bot.send_message(message.chat.id, 'не поняв')

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
                    user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                    user_markup.add("Вернуться на главное меню")
                    await bot.send_message(message.chat.id, 'Введенное имя содержит недопустимые символы!', reply_markup=user_markup)

                    await bot.send_message(message.chat.id, "Введите имя:")

                elif user_status == 'student' and name.isalpha() == True and len(name)<=15:
                    name = name.capitalize()
                    dict_of_param["student_name"] = name
                    json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
                    user_info = json_work_new.get_info_about_unregistered_student(user_id)
                    await bot.send_message(message.chat.id, "Отлично! Ваше имя успешно изменено")
                    await bot.send_message(message.chat.id, user_info)
                elif len(name)<=15:
                    name = name.capitalize()
                    dict_of_param["teacher_name"] = name
                    json_work_new.add_info_about_unregistered_teacher(dict_of_param, user_id)
                    user_info = json_work_new.get_info_about_unregistered_teacher(user_id)


                    await bot.send_message(message.chat.id, "Отлично! Ваше имя успешно изменено")
                    await bot.send_message(message.chat.id, user_info)

                user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

                if user_status == 'student':
                    user_info = json_work_new.get_info_about_unregistered_student(user_id)

                    user_markup.add('Изменить имя', 'Изменить фамилию')
                    user_markup.add('Изменить факультет', 'Изменить курс')
                    user_markup.add('Изменить группу')
                    if dict_of_param["student_group"] != '':
                        if json_work_new.group_has_headmen(dict_of_param["student_group"]) and dict_of_param['status'] == 'Студент 🤓':
                            user_markup.add("Назначить себя старостой 🤠")

                    if dict_of_param["status"] == 'Староста 🤠':
                        user_markup.add("Назначить себя студентом 🤓")

                    if json_work_new.is_valid(dict_of_param):
                        user_markup.add('Завершить регистрацию')
                    user_markup.add('Задать вопрос или сообщить об ошибке')
                    user_markup.add('Отменить регистрацию')

                else:
                    user_info = json_work_new.get_info_about_unregistered_teacher(user_id)

                    user_markup.add('Изменить имя', 'Изменить фамилию')
                    user_markup.add('Изменить отчество')
                    if json_work_new.is_valid(dict_of_param):
                        user_markup.add('Завершить регистрацию')
                    user_markup.add('Задать вопрос или сообщить об ошибке')
                    user_markup.add('Отменить регистрацию')

                await bot.send_message(message.chat.id, "Выберите пункт меню", reply_markup=user_markup) 
                #Обнуление последних сообщение бота!               
            elif json_work_new.get_last_user_command_un(user_id) == "Изменить фамилию":
                name = message.text
                user_status = json_work_new.get_user_status_un(user_id)
                if user_status == 'student':
                    dict_of_param = json_work_new.get_info_about_unregistered_student_dict(user_id)
                else:
                    dict_of_param = json_work_new.get_info_about_unregistered_teacher_dict(user_id)

                if name.isalpha() == False or len(name)>15:
                    user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                    user_markup.add("Вернуться на главное меню")
                    await bot.send_message(message.chat.id, 'Введенная фамилия содержит недопустимые символы!', reply_markup=user_markup)

                    await bot.send_message(message.chat.id, "Введите фамилию:")         

                elif user_status == 'student' and name.isalpha() == True and len(name)<=15:
                    name = name.capitalize()
                    dict_of_param["student_family_name"] = name
                    json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
                    user_info = json_work_new.get_info_about_unregistered_student(user_id)
                    await bot.send_message(message.chat.id, "Отлично! Ваша фамилия успешно изменена")
                    await bot.send_message(message.chat.id, user_info)
                    json_work_new.update_last_user_command_un(user_id,'')
                else:
                    name = name.capitalize()
                    dict_of_param["teacher_family_name"] = name
                    json_work_new.add_info_about_unregistered_teacher(dict_of_param, user_id)
                    user_info = json_work_new.get_info_about_unregistered_teacher(user_id)


                    await bot.send_message(message.chat.id, "Отлично! Ваша фамилия успешно изменена")
                    await bot.send_message(message.chat.id, user_info)

                user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

                if user_status == 'student':
                    user_info = json_work_new.get_info_about_unregistered_student(user_id)

                    user_markup.add('Изменить имя', 'Изменить фамилию')
                    user_markup.add('Изменить факультет', 'Изменить курс')
                    user_markup.add('Изменить группу')

                    if dict_of_param["student_group"] != '':
                        if json_work_new.group_has_headmen(dict_of_param["student_group"]) and dict_of_param['status'] == 'Студент 🤓':
                            user_markup.add("Назначить себя старостой 🤠")

                    if dict_of_param["status"] == 'Староста 🤠':
                        user_markup.add("Назначить себя студентом 🤓")

                    if json_work_new.is_valid(dict_of_param):
                        user_markup.add('Завершить регистрацию')
                    user_markup.add('Задать вопрос или сообщить об ошибке')
                    user_markup.add('Отменить регистрацию')

                else:
                    user_info = json_work_new.get_info_about_unregistered_teacher(user_id)

                    user_markup.add('Изменить имя', 'Изменить фамилию')
                    user_markup.add('Изменить отчество')
                    if json_work_new.is_valid(dict_of_param):
                        user_markup.add('Завершить регистрацию')
                    user_markup.add('Задать вопрос или сообщить об ошибке')
                    user_markup.add('Отменить регистрацию')

                await bot.send_message(message.chat.id, "Выберите пункт меню", reply_markup=user_markup) 
                
                #Обнуление последних сообщений бота
            elif json_work_new.get_last_user_command_un(user_id) == "Изменить отчество":
                name = message.text
                user_status = json_work_new.get_user_status_un(user_id)
                dict_of_param = json_work_new.get_info_about_unregistered_teacher_dict(user_id)
                    
                if name.isalpha() == False or len(name)>15:
                    
                    user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                    user_markup.add("Вернуться на главное меню")
                    await bot.send_message(message.chat.id, 'Отчество содержит недопустимые символы!', reply_markup=user_markup)

                    await bot.send_message(message.chat.id, "Введите отчество:")

                if name.isalpha() == True and len(name)<=15:
                    name = name.capitalize()
                    dict_of_param["teacher_father_name"] = name
                    json_work_new.add_info_about_unregistered_teacher(dict_of_param, user_id)
                    user_info = json_work_new.get_info_about_unregistered_teacher(user_id)


                    await bot.send_message(message.chat.id, "Отлично! Ваше отчество успешно изменено")
                    await bot.send_message(message.chat.id, user_info)

                user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

                user_info = json_work_new.get_info_about_unregistered_teacher(user_id)

                user_markup.add('Изменить имя', 'Изменить фамилию')
                user_markup.add('Изменить отчество')
                if json_work_new.is_valid(dict_of_param):
                    user_markup.add('Завершить регистрацию')
                user_markup.add('Задать вопрос или сообщить об ошибке')
                user_markup.add('Отменить регистрацию')

                await bot.send_message(message.chat.id, "Выберите пункт меню", reply_markup=user_markup) 
                
                #Обнуление последних сообщений бота

            elif json_work_new.get_last_user_command_un(user_id) == "Изменить группу": 
                dict_of_param = json_work_new.get_info_about_unregistered_student_dict(user_id)
                if dict_of_param["name_of_faculty"] != '' and dict_of_param["year_of_study"] != '':
                    if message.text in json_work_new.get_list_of_group(dict_of_param["name_of_faculty"],dict_of_param["year_of_study"])[1]:
                        dict_of_param["student_group"] = message.text
                        json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
                        await bot.send_message( message.chat.id, "Отлично! Ваша группа успешно изменена")
                else:
                    await bot.send_message(message.chat.id, "Сначала заполните поля факультета и курса!😡")
                    
                user_info = json_work_new.get_info_about_unregistered_student(user_id)
                await bot.send_message(message.chat.id, user_info)
                                        
                user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                user_markup.add('Изменить имя', 'Изменить фамилию')
                user_markup.add('Изменить факультет', 'Изменить курс')
                user_markup.add('Изменить группу')
                if dict_of_param["student_group"] != '':
                    if json_work_new.group_has_headmen(dict_of_param["student_group"])  and dict_of_param['status'] == 'Студент 🤓':
                        user_markup.add("Назначить себя старостой 🤠")

                if dict_of_param["status"] == 'Староста 🤠':
                    user_markup.add("Назначить себя студентом 🤓")

                if json_work_new.is_valid(dict_of_param):
                    user_markup.add('Завершить регистрацию')
                user_markup.add('Задать вопрос или сообщить об ошибке')
                user_markup.add('Отменить регистрацию')
                await bot.send_message(message.chat.id, "Выберите пункт меню", reply_markup=user_markup)
            elif json_work_new.get_last_user_command_un(user_id) == 'Задать вопрос или сообщить об ошибке':
                user_msg = f'Пользователь задал вам вопрос или сообщил об ошибке {message.text}'
                for dev_id in ["1254134824", "507634108", "215080778"]:
                    if json_work_new.user_is_registered(dev_id):
                        keyboard = types.InlineKeyboardMarkup()
                        callback_button = types.InlineKeyboardButton(text="Ответить на сообщение", callback_data='Р' + user_id + ' ' + str(message.message_id))
                        keyboard.add(callback_button)
                        await bot.send_message(int(dev_id), user_msg, reply_markup=keyboard)
                await bot.send_message(message.chat.id, "Ваше сообщение доставлено разработчикам! Они постараются вам в ближайшее время ответить")
                user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
                user_markup.add("/help")
                await bot.send_message(message.chat.id, "Введите /help для получения списка команд", reply_markup=user_markup)
                json_work_new.update_last_user_command_un(message.chat.id, "")
                '''Обнуление последней команды и последнего сообщения бота'''

        else:
            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            user_markup.add('Зарегистрироваться как студент 🤓')
            user_markup.add('Зарегистрироваться как преподаватель 👨‍🏫👩‍🏫')
            await bot.send_message(message.chat.id, "Я не понял что ты написал\nТак что го регаться:)", reply_markup=user_markup)















@dp.message_handler(content_types=['document'])
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)

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
                        keyboard = types.InlineKeyboardMarkup()
                        callback_button = types.InlineKeyboardButton(text="Ответить на сообщение", callback_data=user_id + ' ' + str(message.message_id))
                        keyboard.add(callback_button)
                        callback_button = types.InlineKeyboardButton(text="Отправить файл", callback_data='Ф' + user_id + ' ' + str(message.message_id))
                        keyboard.add(callback_button)
                        callback_button = types.InlineKeyboardButton(text="Не отвечать на сообщение", callback_data="nothing")
                        keyboard.add(callback_button)
                        await bot.send_message( message.chat.id, teachers_msg, reply_markup=keyboard)
                    else:
                        await bot.send_message( message.chat.id, teachers_msg)
                else:
                    await bot.send_message( message.chat.id, teachers_msg)
                await bot.send_message( message.chat.id, message.document.file_id)

            await bot.send_message( message.chat.id, f"Ваше сообщение вместе с файлом успешно доставлены студентам группы {student_group}!")
            
            user_markup = types.ReplyKeyboardMarkup(True, True)
            user_markup.add('Получить список студентов')
            user_markup.add('Отправить сообщение студентам')
            user_markup.add('Отправить файл студентам')
            user_markup.add('Задать вопрос или сообщить об ошибке')
            user_markup.add('Удалить профиль')

            await bot.send_message( message.chat.id, 'Выберите пункт меню:', reply_markup=user_markup)
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
            
                keyboard = types.InlineKeyboardMarkup()
                callback_button = types.InlineKeyboardButton(text="Ответить на сообщение", callback_data='С' + user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = types.InlineKeyboardButton(text="Отправить файл", callback_data='ФС' + user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = types.InlineKeyboardButton(text="Не отвечать на сообщение", callback_data="nothing")
                keyboard.add(callback_button)
                await bot.send_message(int(headmen_id_info[0]), student_msg, reply_markup=keyboard, reply_to_message_id=int(headmen_id_info[3]))
                await bot.send_document(int(headmen_id_info[0]), message.document.file_id)
                await bot.send_message( message.chat.id, "Ваше сообщение и файл успешно доставлены старосте!")
            else:
                await bot.send_message( message.chat.id, "Староста уже удален из базы😥")

            
            bot.edit_message_text(chat_id=message.chat.id, message_id=int(headmen_id_info[1]), text=headmen_id_info[2])
  
            user_markup = types.ReplyKeyboardMarkup(True, True)
            user_markup.add('Получить расписание')
            user_markup.add('Получить список студентов своей группы')
            user_markup.add('Задать вопрос или сообщить об ошибке')
            user_markup.add('Удалить профиль')

            await bot.send_message( message.chat.id, 'Выберите действие:', reply_markup=user_markup)
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
                keyboard = types.InlineKeyboardMarkup()
                callback_button = types.InlineKeyboardButton(text="Ответить на сообщение", callback_data=user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = types.InlineKeyboardButton(text="Не отвечать на сообщение", callback_data="nothing")
                keyboard.add(callback_button)
                await bot.send_message(int(teacher_id_info[0]), text, reply_markup=keyboard, reply_to_message_id=int(teacher_id_info[3]))
                await bot.send_message( message.chat.id, "Ваше сообщение вместе с файлом успешно доставлены преподавателю!")
            else:
                await bot.send_message( message.chat.id, "Преподаватель уже удален из базы😥")

            await bot.send_document(int(teacher_id_info[0]), message.document.file_id)

            await bot.edit_message_text(chat_id=message.chat.id, message_id=int(teacher_id_info[1]), text=teacher_id_info[2])

            user_markup = types.ReplyKeyboardMarkup(True, True)
            user_markup.add('Получить расписание')
            if user_status == 'Староста 🤠':
                user_markup.add('Получить список студентов своей группы')
                user_markup.add('Отправить сообщение своим студентам')
                user_markup.add('Отправить файл своим студентам')
                user_markup.add('Изменить расписание')
            else:
                user_markup.add('Получить список студентов своей группы')
            user_markup.add('Задать вопрос или сообщить об ошибке')
            user_markup.add('Удалить профиль')
            await bot.send_message( message.chat.id, 'Выберите действие:', reply_markup=user_markup)
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
                keyboard = types.InlineKeyboardMarkup()
                callback_button = types.InlineKeyboardButton(text="Ответить на сообщение", callback_data='С' + user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = types.InlineKeyboardButton(text="Отправить файл", callback_data='Ф' + user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = types.InlineKeyboardButton(text="Не отвечать на сообщение", callback_data="nothing")
                keyboard.add(callback_button)
                bot.send_message(student_id, headman_text_for_students, reply_markup=keyboard)
                bot.send_document(student_id, message.document.file_id)

                
            await bot.send_message( message.chat.id, "Ваше сообщение и файл успешно доставлены студенту вашей группы!")

            user_markup = types.ReplyKeyboardMarkup(True, True)
            user_markup.add('Получить расписание')
            user_markup.add('Получить список студентов своей группы')
            user_markup.add('Отправить сообщение своим студентам')
            user_markup.add('Отправить файл своим студентам')
            user_markup.add('Изменить расписание')
            user_markup.add('Задать вопрос или сообщить об ошибке')
            user_markup.add('Удалить профиль')
            await bot.send_message( message.chat.id, 'Выберите действие:', reply_markup=user_markup)
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
                keyboard = types.InlineKeyboardMarkup()
                callback_button = types.InlineKeyboardButton(text="Ответить на сообщение", callback_data='С' + user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = types.InlineKeyboardButton(text="Отправить файл", callback_data='Ф' + user_id + ' ' + str(message.message_id))
                keyboard.add(callback_button)
                callback_button = types.InlineKeyboardButton(text="Не отвечать на сообщение", callback_data="nothing")
                keyboard.add(callback_button)
                bot.send_message(student_id, headman_text_for_students, reply_markup=keyboard)
                bot.send_document(student_id, message.document.file_id)

                
            await bot.send_message( message.chat.id, "Ваше сообщение и файл успешно доставлены студентам вашей группы!")

            user_markup = types.ReplyKeyboardMarkup(True, True)
            user_markup.add('Получить расписание')
            user_markup.add('Получить список студентов своей группы')
            user_markup.add('Отправить сообщение своим студентам')
            user_markup.add('Отправить файл своим студентам')
            user_markup.add('Изменить расписание')
            user_markup.add('Задать вопрос или сообщить об ошибке')
            user_markup.add('Удалить профиль')
            await bot.send_message( message.chat.id, 'Выберите действие:', reply_markup=user_markup)
            json_work_new.update_last_user_command_s(user_id, "")
            json_work_new.update_last_bot_msg_s(user_id, "")
            json_work_new.update_last_user_id_s(user_id, [])
            json_work_new.update_student_msg(user_id, '')

        

@dp.callback_query_handler(lambda call: True)
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)
    
    if call.message:
        print(call.data)
        if call.data != "nothing":
            user_status = json_work_new.get_user_status(user_id)
            user_and_message_id = call.data.split()
            user_markup = types.ReplyKeyboardMarkup(True, True)
            if 'Р' in call.data:
                if user_status == 'Учитель 👨‍🏫👩‍🏫':
                    json_work_new.update_last_user_command_t(user_id, 'Ответить на сообщение пользователя')
                    #json_work_new.update_last_user_id_t(user_id, [user_and_message_id[0][1:], call.message.message.chat.id, call.message.text, user_and_message_id[1]])
                    json_work_new.update_last_user_id_s(user_id, [user_and_message_id[0][2:], call.message.message_id, call.message.text, user_and_message_id[1]])
                    #json_work_new.update_last_user_id_t(user_id, [user_and_message_id[0][1:])
                else:
                    json_work_new.update_last_user_command_s(user_id, 'Ответить на сообщение пользователя')
                    #json_work_new.update_last_user_id_s(user_id, [user_and_message_id[0][1:], call.message.message.chat.id, call.message.text user_and_message_id[1]])
                    #json_work_new.update_last_user_id_s(user_id, [user_and_message_id[0][1:])
                user_markup.add("Отменить действие")
                await bot.send_message( message.chat.id, "Введите сообщение:", reply_markup=user_markup)


            elif user_status != 'Учитель 👨‍🏫👩‍🏫':
                if 'С' in call.data:
            
                    if call.data[0] == 'С': # С - на русском!!!!!

                        if user_status == "Староста 🤠":
                            json_work_new.update_last_user_command_s(user_id, "Ответить на сообщение студента")
                        else:
                            json_work_new.update_last_user_command_s(user_id, "Ответить на сообщение старосты")
                        user_markup.add("Отменить действие")
                        json_work_new.update_last_user_id_s(user_id, [user_and_message_id[0][1:], call.message.message_id, call.message.text, user_and_message_id[1]])
                        #json_work_new.update_last_user_id_s(user_id, [user_and_message_id[0][1:])
                        await bot.send_message( message.chat.id, "Введите сообщение:", reply_markup=user_markup)
                        return

                    elif call.data[0] == 'Ф':
                        if user_status == "Староста 🤠":
                            json_work_new.update_last_user_command_s(user_id, "Отправить файл студенту")
                        else:
                            json_work_new.update_last_user_command_s(user_id, "Отправить файл старосте")
                        user_markup.add("Отменить действие")
                        json_work_new.update_last_user_id_s(user_id, [user_and_message_id[0][2:], call.message.message_id, call.message.text, user_and_message_id[1]])
                        #json_work_new.update_last_user_id_s(user_id, [user_and_message_id[0][2:])
                        await bot.send_message( message.chat.id, "Введите сообщение, которое прийдет вместе с вашим файлом:", reply_markup=user_markup)
                        return

                    else:


                        json_work_new.update_last_user_command_s(user_id, "Ответить на сообщение")
                        json_work_new.update_last_user_id_s(user_id, [user_and_message_id[0], call.message.message_id, call.message.text, user_and_message_id[1]])

                elif call.data[0][0] == 'Ф':
                    json_work_new.update_last_bot_msg_s(user_id, "Введите сообщение, которое прийдет вместе с вашим файлом:")
                    json_work_new.update_last_user_id_s(user_id, [user_and_message_id[0][1:], call.message.message_id, call.message.text, user_and_message_id[1]])
                    #json_work_new.update_last_user_id_s(user_id, [user_and_message_id[0][1:])
                    user_markup.add("Отменить действие")
                    await bot.send_message( message.chat.id, "Введите сообщение, которое прийдет вместе с вашим файлом:", reply_markup=user_markup)
                    return
                else:
                    json_work_new.update_last_user_command_s(user_id, "Ответить на сообщение")
                    json_work_new.update_last_user_id_s(user_id, [user_and_message_id[0], call.message.message_id, call.message.text, user_and_message_id[1]])
                    #json_work_new.update_last_user_id_s(user_id, [user_and_message_id[0])
                    user_markup.add("Отменить действие")
                    await bot.send_message( message.chat.id, "Введите сообщение:", reply_markup=user_markup)
                    return

            else:
                
                if call.data[0][0] == 'Ф':
                    json_work_new.update_last_user_id_t(user_id, [user_and_message_id[0][1:], call.message.message_id, call.message.text, user_and_message_id[1]])
                    #json_work_new.update_last_user_id_t(user_id, [user_and_message_id[0][1:])
                    json_work_new.update_last_bot_msg_t(user_id, "Введите сообщение, которое прийдет вместе с вашим файлом:")
                    user_markup.add("Отменить действие")
                    await bot.send_message( message.chat.id, "Введите сообщение, которое прийдет вместе с вашим файлом:", reply_markup=user_markup)
                else:
                    #json_work_new.update_last_user_id_t(user_id, [user_and_message_id[0])
                    json_work_new.update_last_user_id_t(user_id, [user_and_message_id[0], call.message.message_id, call.message.text, user_and_message_id[1]])
                    json_work_new.update_last_user_command_t(user_id, "Ответить на сообщение")
                    user_markup.add("Отменить действие")
                    await bot.send_message( message.chat.id, "Введите сообщение:", reply_markup=user_markup)

            
            
        else:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=call.message.message_id, text=call.message.text)



'''@dp.message_handler(func=lambda mess:  "CAACAgIAAxkBAAMoX5xojUxJPp4CRoNdwzSri3jP1M0AAiwCAAIh7bsD0QLdh-0eCW0bBA"== message.text )
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
    executor.start_polling(dp, skip_updates=True)
