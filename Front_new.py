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
    #user_id = str(message.from_user.id)
    user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    user_markup.add('help')
    
    #await message.reply("С возвращением! Используйте команду /help для получения списка доступных команд.",  reply_markup=user_markup)   
    await message.reply( message.chat.first_name,  reply_markup=user_markup)  
    #await message.reply("С возвращением! Используйте команду /help для получения списка доступных команд.")  '''
    
@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)

    if json_work_new.user_is_registered(user_id):
        #user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        #user_markup.add('/help')
        await message.reply("С возвращением! Используйте команду /help для получения списка доступных команд.")

    else:
        user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        user_markup.add('Зарегистрироваться как студент 🤓')
        user_markup.add('Зарегистрироваться как преподаватель 👨‍🏫👩‍🏫')
        await message.reply(f"Здравствуй, {message.chat.first_name}! 😃\nИспользуй кнопки ниже, чтобы начать процесс регистрации в нашем боте👨‍💻👩‍💻", reply_markup=user_markup) 

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
        await message.reply('Выберите пункт меню:', reply_markup=user_markup)

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

                await message.reply(user_info, reply_markup=user_markup)

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
                
                await message.reply(user_info, reply_markup=user_markup)
        else:
            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            user_markup.add('Зарегистрироваться как студент 🤓')
            user_markup.add('Зарегистрироваться как преподаватель 👨‍🏫👩‍🏫')
            await message.reply( "Вас нет в базе! Давайте регаться:)", reply_markup=user_markup) 
            

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
    await message.reply('Выберите пункт меню:', reply_markup=user_markup)


@dp.message_handler(lambda message: message.text== 'Отправить сообщение своим студентам')
async def cmd_start(message: types.Message):
        user_id = str(message.chat.id) 
        user_status = json_work_new.get_user_status(user_id)

        if user_status == 'Староста 🤠' :
            #if last_command == 
            json_work_new.update_last_user_command_s(user_id, message.text)
            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            user_markup.add('Отменить действие')
            await message.reply('Введите сообщение:', reply_markup=user_markup)

        else:
            if user_status == 'Студент 🤓':
                json_work_new.update_last_user_command_s(user_id, "")

            elif user_status == 'Учитель 👨‍🏫👩‍🏫':
                json_work_new.update_last_user_command_t(user_id, "")

            await message.reply("Отказано в доступе")
            
            
@dp.message_handler(lambda message: message.text== 'Задать вопрос или сообщить об ошибке')
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)
    if json_work_new.user_is_registered(user_id):
        user_status = json_work_new.get_user_status(user_id)
        if user_status != 'Учитель 👨‍🏫👩‍🏫':
            json_work_new.update_last_user_command_s(user_id, 'Задать вопрос или сообщить об ошибке')
        else:
            json_work_new.update_last_user_command_t(user_id, 'Задать вопрос или сообщить об ошибке')
        await message.reply("Введите сообшение, которое будет доставлено разработчику:")
    else:
        json_work_new.update_last_user_command_un(user_id, 'Задать вопрос или сообщить об ошибке')
        await message.reply("Введите сообшение, которое будет доставлено разработчику:")
        
        
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

        await message.reply('Выберите день:', reply_markup=user_markup)
    else:
        json_work_new.update_last_user_command_t(user_id, "")
        await message.reply('Отказано в доступе')
        
        
@dp.message_handler(lambda message: message.text== 'Получить список студентов своей группы' )
async def cmd_start(message: types.Message):
    user_id = str(message.chat.id)   
    user_status = json_work_new.get_user_status(user_id)

    if user_status == 'Староста 🤠' or user_status == 'Студент 🤓':
        student_group = json_work_new.get_student_group(user_id)
        group_list = json_work_new.get_group_list(student_group)
        await message.reply(group_list)

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
        await message.reply('Выберите действие:', reply_markup=user_markup)

    else:
        if user_status == 'Учитель 👨‍🏫👩‍🏫':
            json_work_new.update_last_user_command_t(user_id, "")

        await message.reply("Отказано в доступе")


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
        await message.reply( 'Выберите факультет:', reply_markup=user_markup)

    else:
        json_work_new.update_last_user_command_s(user_id, "")
        await message.reply( "Отказано в доступе")
       
       
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
        await message.reply('Студенты смогут ответить на ваше сообщение?', reply_markup=user_markup)

    else:
        json_work_new.update_last_user_command_s(user_id, "")
        await message.reply( "Отказано в доступе")
        
        
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
            
            await message.reply(  'Выберите курс:', reply_markup=user_markup)

        else:
            json_work_new.update_last_user_command_s(user_id, "")
            await message.reply("Отказано в доступе")
            
    elif json_work_new.user_in_unregistered_list(user_id):
        if json_work_new.get_last_user_command_un(user_id) == "Изменить факультет":
            dict_of_param = json_work_new.get_info_about_unregistered_student_dict(user_id)
            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            if message.text in json_work_new.get_list_of_faculties():
                dict_of_param["name_of_faculty"] = message.text
                dict_of_param["student_group"] = ''
                dict_of_param["year_of_study"] = ''
                await message.reply("Отлично! Ваш факультет успешно изменен. Если вы ранее заполняли поля группа или курс, пожалуйста, заполните их заново")
                json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
            user_info = json_work_new.get_info_about_unregistered_student(user_id)
            await message.reply(user_info)
                
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
            await message.reply( "Выберите пункт меню", reply_markup=user_markup)
           

@dp.message_handler(lambda message: message.text == '1 курс' or message.text == '2 курс' or message.text == '3 курс' or message.text == '4 курс' or message.text == '5 курс' or message.text == '6 курс')
async def cmd_start(message: types.Message):     
    user_id = str(message.chat.id)  

    if json_work_new.user_is_registered(user_id): 
        user_status= json_work_new.get_user_status(user_id)
        year_of_study = message.text[0]
        
        if user_status == 'Учитель 👨‍🏫👩‍🏫':
            #json_work_new.update_last_user_command_t(user_id, "Получить список студентов")
            faculty = json_work_new.get_chosen_faculty(user_id)
            json_work_new.update_chosen_faculty(user_id, "")
            list_of_groups_text, list_of_groups = json_work_new.get_list_of_group(faculty, year_of_study)
            await message.reply(list_of_groups_text)
            last_teacher_command = json_work_new.get_last_user_command_t(user_id)

            user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

            if len(list_of_groups):
                for name_of_group in list_of_groups:
                    user_markup.add(name_of_group)          
                
                user_markup.add('Отменить действие')

                if last_teacher_command == 'Получить список студентов':
                    bot_msg = 'Выберите название группы, список студентов которой вы хотите получить'
                elif last_teacher_command == 'Отправить сообщение студентам':
                    bot_msg = "Выберите название группы, сутдентам которой вы хотите отправить сообщение"
                elif last_teacher_command == 'Отправить файл студентам':
                    bot_msg = "Выберите название группы, сутдентам которой вы хотите отправить файл"

                await message.reply(bot_msg, reply_markup=user_markup)
                json_work_new.update_last_bot_msg_t(user_id, bot_msg)

            else:
                user_markup.add('Получить список студентов')
                user_markup.add('Отправить сообщение студентам')
                user_markup.add('Отправить файл студентам')
                user_markup.add('Задать вопрос или сообщить об ошибке')
                user_markup.add('Удалить профиль')
                await message.reply('Выберите действие', reply_markup=user_markup)

        else:
            json_work_new.update_last_user_command_s(user_id, "")
            await message.reply("Отказано в доступе")

    elif json_work_new.user_in_unregistered_list(user_id):
        if json_work_new.get_last_user_command_un(user_id) == "Изменить курс":   
            dict_of_param = json_work_new.get_info_about_unregistered_student_dict(user_id)
            if dict_of_param["name_of_faculty"] != '':
                dict_of_param["year_of_study"] = message.text[0]
                dict_of_param["student_group"] = ''
                await message.reply("Отлично! Ваш курс успешно изменен. Если вы ранее заполняли поля группа, пожалуйста, заполните её заново")
                json_work_new.add_info_about_unregistered_student(dict_of_param, user_id)
                user_info = json_work_new.get_info_about_unregistered_student(user_id)
                await message.reply(user_info)

            
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
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
            await message.reply(reply_markup=user_markup)

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
        await message.reply('Выберите пункт меню:', reply_markup=user_markup)
    
    else:
        json_work_new.update_last_user_command_t(user_id, "")
        await message.reply("Отказано в доступе")
    

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
            await message.reply(info, reply_markup=user_markup)

        else:
            await message.reply("Вы уже начинали процесс регистрации")
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

                await message.reply(user_info, reply_markup=user_markup)

            else:
                user_info = json_work_new.get_info_about_unregistered_teacher(user_id)
                dict_of_param = json_work_new.get_info_about_unregistered_teacher_dict(user_id)

                user_markup = telebot.types.ReplyKeyboardMarkup(True, False)

                user_markup.add('Изменить имя', 'Изменить фамилию')
                user_markup.add('Изменить отчество')
                if json_work_new.is_valid(dict_of_param):
                    user_markup.add('Завершить регистрацию')
                user_markup.add('Задать вопрос или сообщить об ошибке')
                user_markup.add('Отменить регистрацию')
                
                await message.reply(user_info, reply_markup=user_markup)

    else:
        await message.reply("непонел")
        #Обнуление последних команд 
        
#513

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)