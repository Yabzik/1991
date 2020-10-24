import xlrd
import json

class Parser:
    def __init__(self, path):
        self.book = xlrd.open_workbook(path)
        self.result = {}
        for sheet in range(self.book.nsheets):
            self.result.update(self.process_sheet(self.book.sheet_by_index(sheet)))
    
    def process_sheet(self, sheet):
        result = {}

        group_columns = {}
        for i in range(len(sheet.row_values(7))):
            if isinstance(sheet.row_values(7)[i], float):
                group_columns[int(str(sheet.row_values(7)[i])[:1])] = i

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

        for group, group_col in group_columns.items():
            for day_title, day_row in day_rows.items():
                day = sheet.col_values(group_col)[day_row:day_row+8]
                if len(day) == 8:
                    if not day_title in result:
                        result[day_title] = {}
                    result[day_title][group] = [tuple(day[x:x+2]) for x in range(0, len(day), 2)]

        return result

    def save(self, path):
        with open(path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.result, indent=4, ensure_ascii=False))
            

Parser('timetable/epf/kb-d.xls').save('parsed_timetable/epf/kb-d.json')