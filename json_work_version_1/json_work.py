import json
import datetime as dt

def read_students_file():
    '''Функция для получения базы студентов '''
    with open("json_work_file.json", "r", encoding="utf-8") as f_read:
        text = json.load(f_read)
    return text


def read_timetable_file(code_of_group):
    '''Функция для полученя базы расписаний'''
    with open(f"../parsed_timetable/epf/{code_of_group}-d.json", "r", encoding="utf-8") as f_read:
        text = json.load(f_read)
    return text


def check_user(telegram_id):
    '''Фукнция для проерки наличие студента в базе'''
    list_of_students = read_students_file()["list_of_students"]
    for student_info in list_of_students:
        if student_info["telegram_id"] == telegram_id:
            return (False, "Такой студент уже есть!", student_info)
    else:
        return (True, "Отлично! Мы вас добавили!")



def new_user(dict_of_param):
    '''Функция для добавления нового студента, если его нет в базе'''
    result = check_user(dict_of_param["telegram_id"])
    if result[0]:
        list_of_students = read_students_file()
        list_of_students["list_of_students"].append(dict_of_param)
        with open("json_work_file.json", "w", encoding="utf-8") as f_write:
            json.dump(f_dict, f_write)
    return "Нет такого студента"


def get_timetable(telegram_id, user_weekday):
    '''Фукнция для получения расписания студента в определенный день'''
    result = check_user(telegram_id)
    if not result[0]:
        '''Определения даты дня, который ввёл пользователь'''
        today_d = dt.datetime.date(dt.datetime.now())
        weekday_now = today_d.isoweekday()
        diff = user_weekday - weekday_now
        diff = dt.timedelta(days = diff)
        user_date = today_d + diff
        user_date_str = user_date.strftime("%d.%m.%Y")
        '''Составления расписания в текстовом виде'''
        tt_file = read_timetable_file(result[2]["code_of_group"])
        timetable_str = ""

        #user_date_str = "25.09.2020"
        if user_date_str in tt_file.keys():
            for lesson in range(4):
                name_of_lesson = tt_file[user_date_str][result[2]["year_of_study"]][lesson][0]
                audience_and_teacher = tt_file[user_date_str][result[2]["year_of_study"]][lesson][1]
                if len(name_of_lesson):
                    timetable_str += f"\nПара номер {lesson + 1}: {name_of_lesson}\nПреподаватель и аудитория: {audience_and_teacher};"
        else:
            return "Для этого дня для тебя не составили расписание("
        if len(timetable_str):
            return timetable_str
        else:
            return "В этот день у тебя нет пар. Спи спокойно)"

    else:
        return result[1]


'''def write():
    with open("json_work_file.json", "w", encoding="utf-8") as f_write:
        pass'''


if __name__ == "__main__": 
   print(get_timetable("251538190", 3))
