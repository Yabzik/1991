import json
import datetime as dt


''' 
    Доступные функции:
    
    get_info_about_student()
    update_last_user_command()
    update_last_bot_msg()
    get_last_user_command()
    get_last_bot_msg()
    get_group_list()
    read_student_file()
    read_timetable_file()
    check_user()
    add_new_user()
    get_timetable()

'''


'''def get_group_list_id(student_grop)
    Получение списка идентификаторов студентов определенной группы для дальнейшей обработки

    return None
'''


def get_info_about_student(telegram_id):
    '''Функция для получения информации о студенте'''
    list_of_students = read()["list_of_students"]
    los = list_of_students["telegram_id"]
    
    info = f'''\tИнформация о студенте:
    Имя: {los["sudent_name"]}
    Фамилия: {los["sutdent_family_name"]}
    Факультет: {los["name_of_faculty"]}
    Курс: {los["year_of_study"]}
    Группа: {los["student_group"]}
    Статус: {los["status"]}
    Звание: {los["rank"]}'''
    
    return info


def update_last_user_command(telegram_id, command):
    '''Функция для обновления последней команды, которую вводил пользователь'''
    file_work = read()
    file_work["list_of_students"][telegram_id]["last_user_command"] = command

    with open("json_work_file.json", "w", encoding="utf-8") as f_write:
            json.dump(file_work, f_write)
    
    return


def update_last_bot_msg(telegram_id, msg):
    '''Функция для обновления последнего сообщения, которое отправлял бот'''
    file_work = read()
    file_work["list_of_students"][telegram_id]["last_bot_msg"] = msg

    with open("json_work_file.json", "w", encoding="utf-8") as f_write:
            json.dump(file_work, f_write)
    
    return


def get_last_user_command(telegram_id):
    '''Функция для получения последней команды, которую вводил пользователь'''
    student_info = read()["list_of_students"][telegram_id]
    
    return student_info["last_user_command"]


def get_last_bot_msg(telegram_id):
    '''Функция для получения последней последнего сообщения, которое отправлял бот'''
    student_info = read()["list_of_students"][telegram_id]
    
    return student_info["last_bot_msg"]


def get_group_list(student_group):
    '''Функция для получения списка студентов определённой группы'''
    list_of_students = read()["list_of_students"]
    list_of_students_in_group_str = ""
    num_of_student = 1

    for student_telegram_id in list_of_students.keys():
        student_info = list_of_students[student_telegram_id]
        if student_info["student_group"] == student_group:
            list_of_students_in_group_str += f"\n{num_of_student}. {student_info['student_name']} {student_info['sutdent_family_name']}"
            if student_info["status"] == "Староста 🤠":
                list_of_students_in_group_str += " - 🤠"
    
    if len(list_of_students_in_group_str):
        list_of_students_in_group_str = f"\tСписок студентов группы {student_group}:" + list_of_students_in_group_str
    else:
        list_of_students_in_group_str = f"Пока нет зарегестрированных студентов в нашей системе из группы {student_group} 😐"



def read_students_file():
    '''Функция для получения базы студентов '''
    with open("json_work_file.json", "r", encoding="utf-8") as f_read:
        text = json.load(f_read)
    return text


def read_timetable_file(code_of_group):
    '''Функция для полученя базы расписаний'''
    with open(f"../parser_timetable/{code_of_group}-d.json", "r", encoding="utf-8") as f_read:
        text = json.load(f_read)
    return text


def check_user(telegram_id):
    '''Фукнция для проерки наличие студента в базе'''
    list_of_students = read_students_file()["list_of_students"]
    if telegram_id in list_of_students:
        return {"status_value" : False, "status_msg" : "Такой студент уже есть😡!", "student_info" : student_info}
    else:
        return {"status_value" : True, "status_msg" : "Отлично😃! Мы вас добавили в базу 🖥!", "student_info" : student_info}


def add_new_user(dict_of_param, telegram_id):
    '''Функция для добавления нового студента, если его нет в базе'''
    result = check_user(telegram_id)
    if result["staus_value"]:
        list_of_students = read_students_file()
        list_of_students["list_of_students"].append(dict_of_param)
        with open("json_work_file.json", "w", encoding="utf-8") as f_write:
            json.dump(f_dict, f_write)
    return result["status_msg"]


def get_timetable(telegram_id, user_weekday):
    '''Фукнция для получения расписания студента в определенный день'''
    result = check_user(telegram_id)
    if not result["status_value"]:
        '''Определения даты дня, который ввёл пользователь'''
        today_d = dt.datetime.date(dt.datetime.now())
        weekday_now = today_d.isoweekday()
        diff = user_weekday - weekday_now
        diff = dt.timedelta(days = diff)
        user_date = today_d + diff
        user_date_str = user_date.strftime("%d.%m.%Y")
        '''Составления расписания в текстовом виде'''
        tt_file = read_timetable_file(result["student_info"]["code_of_group"])
        timetable_str = ""

        #user_date_str = "25.09.2020"
        if user_date_str in tt_file.keys():
            for lesson in range(4):
                name_of_lesson = tt_file[user_date_str][result[2]["year_of_study"]][lesson][0]
                audience_and_teacher = tt_file[user_date_str][result[2]["year_of_study"]][lesson][1]
                if len(name_of_lesson):
                    timetable_str += f"\nПара номер {lesson + 1}: {name_of_lesson}\nПреподаватель и аудитория: {audience_and_teacher};"
        else:
            return "На этот день для тебя не составили расписание🥺("
        if len(timetable_str):
            return timetable_str
        else:
            return "В этот день у тебя нет пар🙂. Можешь поспать подольше) 😴"

    else:
        return result["status_msg"]


'''def write():
    with open("json_work_file.json", "w", encoding="utf-8") as f_write:
        pass'''


'''if __name__ == "__main__": 
   print(get_timetable("251538190", 3))'''
