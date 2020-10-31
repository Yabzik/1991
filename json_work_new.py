import json
import datetime as dt
import emoji
import requests


''' 
    Доступные функции:
    
    get_list_of_group()
    read_group_data()
    get_user_status()
    get_student_status()
    get_group_list_id()
    get_info_about_student()
    update_last_user_command_s()
    update_last_bot_msg_s()
    get_last_user_command_s()
    get_last_bot_msg_s()
    update_last_user_command_t()
    update_last_bot_msg_t()
    get_last_user_command_t()
    get_last_bot_msg_t()
    get_group_list()
    read_data_file()
    read_timetable_file()
    check_student()
    add_new_student()
    check_teacher()
    add_new_teacher()
    get_timetable()
    find_students()

'''

#telegram_id - STRING!!!!

def is_valid(dict_of_param):
    for param in dict_of_param.keys():
        if param == 'last_user_command' or param == 'last_bot_msg':
            continue
        if dict_of_param[param] == '':
            return False
    else:
        return True


def get_user_status_un(telegram_id):
    user_info = read_data_file()['list_of_unregistered_users'][telegram_id]

    return user_info['user_status']


def get_info_about_unregistered_teacher(telegram_id):
    ''''''
    teacher_info = read_data_file()["list_of_unregistered_users"][telegram_id]
    ti = teacher_info

    teacher_info_text = f'''\tИнформация о преподавателе:
    Имя: {ti["teacher_name"]}
    Фамилия: {ti["teacher_family_name"]}
    Отчество: {ti["teacher_father_name"]}
    '''

    return teacher_info_text


def remove_unregistered_user(telegram_id):
    '''Удаление "незарегестрированного пользователя" из базы'''
    data = read_data_file()
    del data["list_of_unregistered_users"][telegram_id]

    with open("json_test_data.json", "w", encoding="utf-8") as f_write:
        json.dump(data, f_write, ensure_ascii=False)

    return None


def get_student_group(telegram_id):
    '''Функция для получения названия группы студента'''
    student_info = read_data_file()["list_of_students"][telegram_id]

    return student_info["student_group"]

def get_teacher_name_and_father_name(telegram_id):
    '''Функция для получения имя и отчество преподавателя'''
    teacher_info = read_data_file()["list_of_teachers"][telegram_id]

    return f"{teacher_info['teacher_name']} {teacher_info['teacher_father_name']}"

def get_list_of_group(name_of_faculty, year_of_study): #year_of_study - STRING!!!
    '''Функция для получения списка груп определенного факультета и курса'''
    list_of_groups = read_group_data()[name_of_faculty][year_of_study]
    if len(list_of_groups):
        list_of_groups_text = 'Список доступных групп:'
        for num_of_group in range(len(list_of_groups)):
            list_of_groups_text += f"\n{num_of_group + 1}. {list_of_groups[num_of_group]}"
        return list_of_groups_text, list_of_groups
    else:
        return "Групп в выбранном факультете и в выбранном курсе ещё нет в базе(", []


def read_group_data():
    '''Функция для получения базы названий груп'''
    with open("json_group_data.json", "r", encoding="utf-8") as f_read:
        data = json.load(f_read)

    return data


def get_user_status(telegram_id):
    ''' Функция для проверки статуса пользователя'''
    data = read_data_file()
    if telegram_id in data["list_of_students"].keys():
        return get_student_status(telegram_id)
    else:
        return "Учитель 👨‍🏫👩‍🏫"


def get_student_status(telegram_id): 
    '''Функция для получения статуса студента'''
    student_info = read_data_file()["list_of_students"][telegram_id]

    return student_info["status"]


def get_group_list_id(student_group):
    '''Получение списка идентификаторов студентов определенной группы для дальнейшей обработки'''
    list_of_students = read_data_file()["list_of_students"]
    list_of_students_id = []
    
    for telegram_id in list_of_students.keys():
        if list_of_students[telegram_id]["student_group"] == student_group:
            list_of_students_id.append(int(telegram_id))
    
    return list_of_students_id


def get_group_list_id_for_headmen(student_group):
    '''Получение списка идентификаторов студентов определенной группы для дальнейшей обработки (без старосты)'''
    list_of_students = read_data_file()["list_of_students"]
    list_of_students_id = []
    
    for telegram_id in list_of_students.keys():
        if list_of_students[telegram_id]["student_group"] == student_group and list_of_students[telegram_id]["status"] != 'Староста 🤠':
            list_of_students_id.append(int(telegram_id))
    
    return list_of_students_id


def add_info_about_unregistered_student(dict_of_param, telegram_id):
    ''''''
    data = read_data_file()
    data["list_of_unregistered_users"][telegram_id] = dict_of_param
    with open("json_test_data.json", "w", encoding="utf-8") as f_write:
        json.dump(data, f_write, ensure_ascii=False)

    return None

def add_info_about_unregistered_teacher(dict_of_param, telegram_id):
    ''''''
    data = read_data_file()
    data["list_of_unregistered_users"][telegram_id] = dict_of_param
    with open("json_test_data.json", "w", encoding="utf-8") as f_write:
        json.dump(data, f_write, ensure_ascii=False)

    return None


def get_info_about_unregistered_student(telegram_id):
    ''''''
    list_of_unregistered_users = read_data_file()["list_of_unregistered_users"][telegram_id]
    louu = list_of_unregistered_users

    info = f'''\tИнформация о студенте:
    Имя: {louu["student_name"]}
    Фамилия: {louu["student_family_name"]}
    Факультет: {louu["name_of_faculty"]}
    Курс: {louu["year_of_study"]}
    Группа: {louu["student_group"]}
    Статус: {louu["status"]}
    '''

    return info


def get_list_of_faculties():
    '''Функция для получения списка доступных факультетов'''
    list_of_faculties = list(read_group_data().keys())

    return list_of_faculties


def get_info_about_student(telegram_id):
    '''Функция для получения информации о студенте'''
    list_of_students = read_data_file()["list_of_students"]
    los = list_of_students[telegram_id]
    
    info = f'''\tИнформация о студенте:
    Имя: {los["sudent_name"]}
    Фамилия: {los["sutdent_family_name"]}
    Факультет: {los["name_of_faculty"]}
    Курс: {los["year_of_study"]}
    Группа: {los["student_group"]}
    Статус: {los["status"]}
    Звание: {los["rank"]}'''
    
    return info


def update_last_user_command_un(telegram_id, command):
    ''''''
    file_work = read_data_file()
    file_work["list_of_unregistered_users"][telegram_id]["last_user_command"] = command

    with open("json_test_data.json", "w", encoding="utf-8") as f_write:
        json.dump(file_work, f_write, ensure_ascii=False)

    return


def get_info_about_unregistered_teacher_dict(telegram_id):
    ''''''
    user_info = read_data_file()["list_of_unregistered_users"][telegram_id]

    return user_info


def get_info_about_unregistered_student_dict(telegram_id):
    ''''''
    user_info = read_data_file()["list_of_unregistered_users"][telegram_id]

    return user_info


def get_last_bot_msg_un(telegram_id):
    ''''''
    unregistered_user_info = read_data_file()["list_of_unregistered_users"][telegram_id]
    
    return unregistered_user_info["last_bot_msg"]


def update_last_bot_msg_un(telegram_id, command):
    ''''''
    file_work = read_data_file()
    file_work["list_of_unregistered_users"][telegram_id]["last_bot_msg"] = command

    with open("json_test_data.json", "w", encoding="utf-8") as f_write:
        json.dump(file_work, f_write, ensure_ascii=False)

    return


def get_last_user_command_un(telegram_id):
    ''''''
    unregistered_user_info = read_data_file()["list_of_unregistered_users"][telegram_id]
    
    return unregistered_user_info["last_user_command"]


def update_last_user_command_s(telegram_id, command):
    '''Функция для обновления последней команды, которую вводил пользователь'''
    file_work = read_data_file()
    file_work["list_of_students"][telegram_id]["last_user_command"] = command

    with open("json_test_data.json", "w", encoding="utf-8") as f_write:
            json.dump(file_work, f_write, ensure_ascii=False)
    
    return


def update_last_bot_msg_s(telegram_id, msg):
    '''Функция для обновления последнего сообщения, которое отправлял бот'''
    file_work = read_data_file()
    file_work["list_of_students"][telegram_id]["last_bot_msg"] = msg

    with open("json_test_data.json", "w", encoding="utf-8") as f_write:
            json.dump(file_work, f_write, ensure_ascii=False)
    
    return


def get_last_user_command_s(telegram_id):
    '''Функция для получения последней команды, которую вводил пользователь'''
    student_info = read_data_file()["list_of_students"][telegram_id]
    
    return student_info["last_user_command"]


def get_last_bot_msg_s(telegram_id):
    '''Функция для получения последней последнего сообщения, которое отправлял бот'''
    student_info = read_data_file()["list_of_students"][telegram_id]
    
    return student_info["last_bot_msg"]


def update_last_user_command_t(telegram_id, command):
    '''Функция для обновления последней команды, которую вводил пользователь'''
    file_work = read_data_file()
    file_work["list_of_teachers"][telegram_id]["last_user_command"] = command

    with open("json_test_data.json", "w", encoding="utf-8") as f_write:
            json.dump(file_work, f_write, ensure_ascii=False)
    
    return


def update_last_bot_msg_t(telegram_id, msg):
    '''Функция для обновления последнего сообщения, которое отправлял бот'''
    file_work = read_data_file()
    file_work["list_of_teachers"][telegram_id]["last_bot_msg"] = msg

    with open("json_test_data.json", "w", encoding="utf-8") as f_write:
            json.dump(file_work, f_write, ensure_ascii=False)
    
    return


def get_last_user_command_t(telegram_id):
    '''Функция для получения последней команды, которую вводил пользователь'''
    student_info = read_data_file()["list_of_teachers"][telegram_id]
    
    return student_info["last_user_command"]


def get_last_bot_msg_t(telegram_id):
    '''Функция для получения последней последнего сообщения, которое отправлял бот'''
    student_info = read_data_file()["list_of_teachers"][telegram_id]
    
    return student_info["last_bot_msg"]


def get_group_list(student_group):
    '''Функция для получения списка студентов определённой группы'''
    list_of_students = read_data_file()["list_of_students"]
    list_of_students_in_group_str = ""
    num_of_student = 1

    for student_telegram_id in list_of_students.keys():
        student_info = list_of_students[student_telegram_id]
        if student_info["student_group"] == student_group:
            list_of_students_in_group_str += f"\n{num_of_student}. {student_info['student_name']} {student_info['student_family_name']}"
            num_of_student += 1
            if student_info["status"] == "Староста 🤠":
                list_of_students_in_group_str += " - 🤠"
    
    if len(list_of_students_in_group_str):
        list_of_students_in_group_str = f"\tСписок студентов группы {student_group}:" + list_of_students_in_group_str
    else:
        list_of_students_in_group_str = f"Пока нет зарегестрированных студентов в нашей системе из группы {student_group} 😐"

    return list_of_students_in_group_str


def get_chosen_faculty(telegram_id):
    '''Функция для получения выбранного * учителем факультета'''
    teacher_info = read_data_file()["list_of_teachers"][telegram_id]

    return teacher_info["chosen_faculty"]


def update_chosen_faculty(telegram_id, name_of_faculty):
    '''Функция для обновления выбранного * учителем факультета'''
    file_work = read_data_file()
    file_work["list_of_teachers"][telegram_id]["chosen_faculty"] = name_of_faculty

    with open("json_test_data.json", "w", encoding="utf-8") as f_write:
            json.dump(file_work, f_write, ensure_ascii=False)
    
    return


def read_data_file():
    '''Функция для получения базы студентов '''
    with open("json_test_data.json", "r", encoding="utf-8") as f_read:
        text = json.load(f_read)
    return text


def read_timetable_file(code_of_group):
    '''Функция для полученя базы расписаний'''
    with open(f"parsed_timetable/epf/{code_of_group}-d.json", "r", encoding="utf-8") as f_read:
        text = json.load(f_read)

    return text


def group_has_headmen(student_group):
    ''''''
    list_of_students = read_data_file()["list_of_students"]

    for student_info in list_of_students.values():
        if student_info["student_group"] == student_group:
            if student_info["status"] == "Староста 🤠":
                return False
    else:
        return True


def check_student(telegram_id):
    '''Фукнция для проерки наличие студента в базе'''
    list_of_students = read_data_file()["list_of_students"]
    if telegram_id in list_of_students:
        return {"status_value" : False, "status_msg" : "Такой студент уже есть😡!", "student_info" : list_of_students[telegram_id]}
    else:
        return {"status_value" : True, "status_msg" : "Отлично😃! Мы вас добавили в базу 🖥!"}


def read_code_of_group():
    ''''''
    with open("json_code_of_group.json", "r", encoding="utf-8") as f_read:
        text = json.load(f_read)

    return text

def remove_student(telegram_id):
    ''''''
    data = read_data_file()
    del data["list_of_students"][telegram_id]

    with open("json_test_data.json", "w", encoding="utf-8") as f_write:
            json.dump(data, f_write, ensure_ascii=False)

    return None

def remove_teacher(telegram_id):
    ''''''
    data = read_data_file()
    del data["list_of_teachers"][telegram_id]

    with open("json_test_data.json", "w", encoding="utf-8") as f_write:
            json.dump(data, f_write, ensure_ascii=False)

    return None

def get_code_of_group(name_of_faculty):
    code_of_group = read_code_of_group()[name_of_faculty]

    return code_of_group

def add_new_student(dict_of_param, telegram_id):
    '''Функция для добавления нового студента, если его нет в базе'''
    result = check_student(telegram_id)
    
    if result["status_value"]:
        data = read_data_file()
        data["list_of_students"][telegram_id] = dict_of_param
        with open("json_test_data.json", "w", encoding="utf-8") as f_write:
            json.dump(data, f_write, ensure_ascii=False)
    
    return result["status_msg"]


def check_teacher(telegram_id):
    '''Функция доя проверки наличия преподавателя в базе'''
    list_of_teachers = read_data_file()["list_of_teachers"]
    if telegram_id in list_of_teachers:
        teacher_info = list_of_teachers[telegram_id]
        return {"status_value" : False, "status_msg" : "Такой преподаватель уже есть🙁!", "teacher_info" : teacher_info}
    else:
        return {"status_value" : True, "status_msg" : "Отлично😃! Мы вас добавили в базу 🖥!"}


def add_new_teacher(dict_of_param, telegram_id):
    '''Функция для добавления нового преподавателя, если его нет в базе'''
    result = check_teacher(telegram_id)
    
    if result["status_value"]:
        list_of_students = read_data_file()
        list_of_students["list_of_teachers"][telegram_id] = dict_of_param
        with open("json_test_data.json", "w", encoding="utf-8") as f_write:
            json.dump(list_of_students, f_write, ensure_ascii=False)
    
    return result["status_msg"]


def user_in_unregistered_list(telegram_id):
    list_of_unregistered_users = read_data_file()["list_of_unregistered_users"]

    return telegram_id in list_of_unregistered_users.keys()


def user_is_registered(telegram_id):
    '''Функция для проверки наличия пользователя в базе студентов или преподавателей'''
    data = read_data_file()

    return telegram_id in data["list_of_students"] or telegram_id in data["list_of_teachers"]


def get_last_user_id_s(telegram_id):
    student_info = read_data_file()["list_of_students"][telegram_id]

    return student_info['last_id']


def update_last_user_id_s(telegram_id, user_id):
    data = read_data_file()
    data["list_of_students"][telegram_id]["last_id"] = user_id

    with open("json_test_data.json", "w", encoding="utf-8") as f_write:
        json.dump(data, f_write, ensure_ascii=False)

    return None


def get_info_about_student_dict(telegram_id):
    student_info = read_data_file()["list_of_students"][telegram_id]

    return student_info


def get_last_user_id_t(telegram_id):
    teacher_info = read_data_file()["list_of_teachers"][telegram_id]

    return teacher_info['last_id']


def update_last_user_id_t(telegram_id, user_id):
    data = read_data_file()
    data["list_of_teachers"][telegram_id]["last_id"] = user_id

    with open("json_test_data.json", "w", encoding="utf-8") as f_write:
        json.dump(data, f_write, ensure_ascii=False)

    return None


def update_teacher_msg(telegram_id, msg):
    data = read_data_file()
    data["list_of_teachers"][telegram_id]["teacher_msg"] = msg

    with open("json_test_data.json", "w", encoding="utf-8") as f_write:
        json.dump(data, f_write, ensure_ascii=False)

    return None


def get_teacher_msg(telegram_id):
    teacher_info = read_data_file()["list_of_teachers"][telegram_id]

    return teacher_info['teacher_msg']


def update_student_msg(telegram_id, msg):
    data = read_data_file()
    data["list_of_students"][telegram_id]["student_msg"] = msg

    with open("json_test_data.json", "w", encoding="utf-8") as f_write:
        json.dump(data, f_write, ensure_ascii=False)

    return None


def get_student_msg(telegram_id):
    teacher_info = read_data_file()["list_of_students"][telegram_id]

    return teacher_info['student_msg']


def user_is_headmen(telegram_id):
    student_info = read_data_file()["list_of_students"][telegram_id]
    if student_info["status"] == 'Староста 🤠':
        return True
    else:
        return False


def get_timetable(telegram_id, user_weekday=None, date=None):
    '''Фукнция для получения расписания студента в определенный день'''
    result = check_student(telegram_id)
    
    if not result["status_value"]:
        '''Определения даты дня, который ввёл пользователь'''
        if user_weekday:
            today_d = dt.datetime.date(dt.datetime.now())
            weekday_now = today_d.isoweekday()
            diff = user_weekday - weekday_now
            diff = dt.timedelta(days = diff)
            user_date = today_d + diff
            user_date_str = user_date.strftime("%d.%m.%Y")
        elif date:
            user_date_str = date
        '''Составления расписания в текстовом виде'''

        r = requests.get(url='https://yabzik.online/unisystem/public/api/schedule', params={
            'speciality': result["student_info"]["code_of_group"] + '-d',
            'course': result["student_info"]["year_of_study"],
            'date': user_date_str
        })
        schedule = r.json()['schedule']

        timetable_str = ""
        numerals = ['I', 'II', 'III', 'IV']
        if schedule:
            for lesson in schedule:
                name_of_lesson = lesson['title']
                audience_and_teacher = lesson['subtitle']
                if name_of_lesson and len(name_of_lesson):
                    em = emoji.choose(' '.join([name_of_lesson, audience_and_teacher]))
                    timetable_str += f"\n{numerals[lesson['index']-1]}. {em} {name_of_lesson}\nПреподаватель и аудитория: {audience_and_teacher};"
        else:
            return "На этот день для тебя не составили расписание🥺("
        if len(timetable_str):
            return timetable_str
        else:
            return "В этот день у тебя нет пар🙂. Можешь поспать подольше) 😴"

    else:
        return result["status_msg"]

def find_students(query):
    '''Фукнция для получения списка студентов по поисковому запросу'''
    list_of_students = read_data_file()["list_of_students"]
    result = {}
    for telegram_id, student_data in list_of_students.items():
        if student_data.items() >= query.items():
            result[telegram_id] = student_data
    return result


def get_answer_t(telegram_id):
    teacher_info = read_data_file()["list_of_teachers"][telegram_id]

    return teacher_info["answer"]


def update_answer_t(telegram_id, answer):
    data = read_data_file()
    data["list_of_teachers"][telegram_id]["answer"] = answer

    with open("json_test_data.json", "w", encoding="utf-8") as f_write:
        json.dump(data, f_write, ensure_ascii=False)

    return None


def get_answer_s(telegram_id):
    teacher_info = read_data_file()["list_of_students"][telegram_id]

    return teacher_info["answer"]


def update_answer_s(telegram_id, answer):
    data = read_data_file()
    data["list_of_students"][telegram_id]["answer"] = answer

    with open("json_test_data.json", "w", encoding="utf-8") as f_write:
        json.dump(data, f_write, ensure_ascii=False)

    return None


def get_full_group_list():
    '''Функция для получения списка всех групп'''
    data_of_group = read_group_data()
    full_group_list = []
    for faculty in data_of_group.keys():
        for year_of_study in data_of_group[faculty].keys():
            full_group_list += data_of_group[faculty][year_of_study]

    return full_group_list

'''def write():
    with open("json_work_file.json", "w", encoding="utf-8") as f_write:
        pass'''