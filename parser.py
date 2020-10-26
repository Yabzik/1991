import xlrd
import json
import os
import requests

# основы директорий для получения расписания
TIMETABLE_BASE = {
    # 'epf': 'http://elf.mdu.in.ua/ROZKLAD/d/',
    'epf': 'https://yabzik.online/epf/', # testing
}

# файлы расписания в директории факультета
TIMETABLE_SPECS = {
    'epf': ['ekologija-d.xls', 'kb-d.xls', 'mb-d.xls', 'mek-d.xls', 'mo-d.xls', 'mp-d.xls', 'pravo-d.xls', 'pua-d.xls', 'sa-d.xls', 'tr-d.xls', 'ufeb-d.xls', 'hackathon-d.xls'],
}

class Parser:
    def __init__(self, path):
        self.book = xlrd.open_workbook(path)
        self.result = {}
        for sheet in range(self.book.nsheets):
            self.result.update(self.process_sheet(self.book.sheet_by_index(sheet)))
    
    def process_sheet(self, sheet):
        # обработка одного листа
        result = {}

        # получение индексов столбцов с группами
        group_columns = {}
        for i in range(len(sheet.row_values(7))):
            if isinstance(sheet.row_values(7)[i], float):
                group_columns[int(str(sheet.row_values(7)[i])[:1])] = i

        # получение начальных индексов строк с днями
        day_rows = {}
        col_0 = sheet.col_values(0)
        for i in range(len(col_0)):
            if i > 6 and col_0[i] != '':
                day_title = col_0[i].split(' ')[-1]
                if '/' in day_title:
                    titles = day_title.split('/')
                    for title in titles:
                        day_rows[title] = i
                else:
                    day_rows[day_title] = i

        # получение расписания для каждой группы и каждого дня
        for group, group_col in group_columns.items():
            for day_title, day_row in day_rows.items():
                day = sheet.col_values(group_col)[day_row:day_row+8]
                if len(day) == 8:
                    if not day_title in result:
                        result[day_title] = {}
                    result[day_title][group] = [tuple(day[x:x+2]) for x in range(0, len(day), 2)]

        return result

    def save(self, path):
        # сохранение файла расписаня
        with open(path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.result, indent=4, ensure_ascii=False))

def on_change(file):
    # вызывается при изменении файла расписания
    faculty_code = file.split('/')[-1].split('.')[0]
    old_data = None
    new_data = None
    with open(file, encoding='utf-8') as f:
        new_data = json.load(f)
    with open(f'{file}.old', encoding='utf-8') as f:
        old_data = json.load(f)

    for date, date_timetable in new_data.items():
        if date not in old_data:
            print('Появилось расписание на день:', date, faculty_code)
            if notify_callback:
                notify_callback(faculty_code, None)
        else:
            if new_data[date] != old_data[date]:
                for course, course_timetable in date_timetable.items():
                    if new_data[date][course] != old_data[date][course]:
                        print('Изменилось расписание на день:', date, faculty_code, course, new_data[date][course])
                        if notify_callback:
                            notify_callback(faculty_code, course)

def poll():
    # проверка на изменение расписания
    for faculty, base in TIMETABLE_BASE.items():
        for file in TIMETABLE_SPECS[faculty]:
            remote_file = requests.get(base + file).content
            file_title = file.split('.')[0]
            local_path_parsed = f'parsed_timetable/{faculty}/{file_title}.json'
            local_path_raw = f'timetable/{faculty}/{file}'

            if not os.path.exists(local_path_parsed):
                with open(local_path_raw, 'wb') as f:
                    f.write(remote_file)
                Parser(local_path_raw).save(local_path_parsed)
                print(f'Файл {file} был обработан!')
            else:
                local_file = None
                with open(local_path_raw, 'rb') as f:
                    local_file = f.read()
                if local_file != remote_file:
                    print(f'Файл {file} изменился!')
                    with open(local_path_raw, 'wb') as f:
                        f.write(remote_file)
                    os.rename(local_path_parsed, f'{local_path_parsed}.old')
                    Parser(local_path_raw).save(local_path_parsed)
                    on_change(local_path_parsed)
                    os.remove(f'{local_path_parsed}.old')

notify_callback = None

# планировщик для обновления расписания
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
scheduler.add_job(poll, 'interval', minutes=2)
scheduler.start()