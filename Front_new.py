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

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)