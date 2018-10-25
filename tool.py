import pandas as pd
from os.path import dirname, join
import sys
print(sys.getdefaultencoding())
import csv

#temp
from bokeh.models import ColumnDataSource, CustomJS, TableColumn, DateFormatter, Button, DataTable
from bokeh.plotting import figure, output_file, show

def get_team():
    fio=[
      'Мамин-Сибиряк Вадим Вадимович'
     ,'Абрего Андрей Анатольевич'
     ,'Атаман Александр Михайлович'
     ,'Бондарь Евгения Дмитриевна'
     ,'Жако Ксения Юрьевна'
     ,'Задул Игорь Сергеевич'
     ,'Кленов Андрей Владимирович'
     ,'Лемм Роман Александрович'
     ,'Пузыренко Павел Васильевич'
     ,'Кучин Андрей Валерьевич'
     ,'Трубецкая Юлия Андреевна'
     ,'Хоров Евгений Сергеевич'
     ,'Скороходов Павел Александрович'
     ,'Вятка Алексей Михайлович'
     ,'Жицкая Полина Викторовна'
     ,'Замашкин Владислав Владиславович'
     ,'Латунцев Сергей Владимирович '
     ,'Иванова Лилия Ринатовна'
     ,'Смагина Екатерина Александровна'
     ,'Симонова Ирина Вениаминовна'
     ,'Юрченко Андрей Александрович'
     ,'Соколова Анна Сергеевна'
     ,'Андреева Надежда Александровна'
     ,'Кенченков Руслан Игоревич'
     ,'Папаха Любовь Сергеевна'
     ,'Подольская Елена Анатольевна'
     ,'Шуйский Александр Сергеевич'
     ,'Родионова Алиса Орестовна'
     ,'Воронин Алексей Алексеевич'
     ,'Зимин Олег Николаевич'
     ,'Арбузов Алексей Владимирович'
    ]

    dep=[
      'ВВС'
     ,'ВВС Маск'
     ,'ВСС Маск'
     ,'ВВС VIP'
     ,'ВВС АА'
     ,'ВВС АА'
     ,'ВВС Пре'
     ,'ВВС Пре'
     ,'ВВС Пре'
     ,'ВВС Маск'
     ,'ВВС Пре'
     ,'ВВС VIP'
     ,'ЕКЕ'
     ,'ЕКЕ/Эква'
     ,'ЕКЕ/ВВС Пре'
     ,'ЕКЕ/Эква'
     ,'ЕКЕ/Эква'
     ,'ЕКЕ/Эква'
     ,'ЕКЕ/Эква'
     ,'ЕКЕ/Эква'
     ,'ЕКЕ/VIP/Эква'
     ,'ДМБ'
     ,'ДМБ/ТТ'
     ,'ДМБ/VIP'
     ,'ДМБ/ЖЖ'
     ,'ДМБ/Пре'
     ,'ДМБ/VIP'
     ,'~'
     ,'~'
     ,'~'
     ,'~'
    ]
    grey=[
      1
     ,0
     ,0
     ,0
     ,0
     ,0
     ,0
     ,0
     ,0
     ,0
     ,0
     ,0
     ,1
     ,0
     ,0
     ,0
     ,0
     ,0
     ,0
     ,0
     ,0
     ,1
     ,0
     ,0
     ,0
     ,0
     ,0
     ,1
     ,1
     ,1
     ,1
    ]
    return {'fio':fio,'dep':dep,'grey':grey}
#------------------------------------------------------------------------------------
def read_csv(file,splitter=None):
    reader = csv.reader(open(file, 'r'))
    dict = {}
    flag = 0
    for row in reader:
        if splitter != None:
            row_str = ''.join(row)  #row является строкой, требуется доп.обработка
            row_list = row_str.split(splitter)
        else:
            row_list = row   #row уже list, доп.обработка не требуется
        if flag == 0:
            header = row_list
            for c in header:
                dict[c] = []
            flag = 1
        else:
            i = 0
            for c in header:
                if i< len(row_list):
                    dict[c].append(row_list[i])
                    i += 1

    return dict

def write_csv(file, data, header, mode='w',check = {}):
    if mode =='a' and check:
        old = read_csv(file)
        count = 0
        flag = 1
        range_col = range(len(old[list(old.keys())[0]]))  # to create empty_column in new keys
        for key_check, val_check in check.items():
            count += 1
            if key_check in old:
                if flag == 1:
                    checker = 'checker'
                    old.update({checker: [0 for i in range_col]})
                    flag = 0
                for it in range(len(old[key_check])):
                    val = old[key_check][it]
                    for i in val_check:
                        if val == i:
                            res = old[checker][it] + 1
                            old[checker][it] = res
        max_result = max(old[checker])
        check_num = len(check)
        new = {}
        if max_result == check_num:
            for key in old.keys():
                if key != checker:
                    new[key] = []
            for i in range(len(old[checker])):
                if old[checker][i] != check_num:
                    for key in old.keys():
                        if key != checker:
                            new[key].append(old[key][i])

            this_header = list(new.keys())
            df = pd.DataFrame(new, columns=this_header)
            df.to_csv(file, encoding='cp1251', index=False,header=this_header, mode='w')
        header = list(data.keys())
        df = pd.DataFrame(data,columns= header)
        df.to_csv(file, encoding='cp1251', index=False, header=False,  mode=mode)
        return

    df = pd.DataFrame(data, columns=header)
    # df.to_csv(myFile,encoding='utf-8', index=False)
    if mode =='a':
        header = False
    df.to_csv(file, encoding='cp1251', index=False, header=header, mode=mode)


def select(key,value,dict_source, header=None):
    slice = [index for index, val in enumerate(dict_source[key]) if val == value]
    dict = {}
    start = slice[0]
    end = slice[-1] + 1
    if header == None:
        for key in dict_source:
           dict[key] = dict_source[key][start:end]
    else:
        for val in header:
            dict[val] = dict_source[val][start:end]
    return dict

def get_max_id(dict,key_id):
    list_id = [int(i) for i in dict[key_id]]
    max_val = max(list_id)
    return max_val

def get_params(mode, calendar=None, team=None, key_year='Year', val_year='2018', key_month='Month_Ru',val_month=None):
    if mode == 'w':
        month = 'Май' #for 31-days header
        calendar_selected = select(key=key_month, value=month, dict_source=calendar)
        config = Config(calendar_selected, team)
        header_dict = config.get_columns(mode='header')
        header_31_days = list(header_dict.keys()) #31-days header
        calendar_selected_year = select(key=key_year, value=val_year, dict_source=calendar)
        calendar_selected_month = select(key=key_month, value=val_month, dict_source=calendar_selected_year)
        config = Config(calendar_selected_month, team)
        data_columns = config.get_columns(mode='data')
        check = {}
        return header_31_days, data_columns, check
    elif mode =='a':
        calendar_selected_year = select(key=key_year, value=val_year, dict_source=calendar)
        calendar_selected_month = select(key=key_month, value=val_month, dict_source=calendar_selected_year)
        data_existed = read_csv(FILE_DATA)
        max_id = get_max_id(dict=data_existed, key_id='id')
        config = Config(calendar_selected_month, team, max_id)
        data_columns = config.get_columns(mode='data')
        header_fact = list(data_columns.keys())
        check = {'year': [val_year], 'month': [val_month]}
        return header_fact, data_columns, check
    elif mode == 'r':
        data_existed = read_csv(FILE_DATA)
        data_selected_year = select(key=key_year, value=val_year, dict_source=data_existed)
        data_columns = select(key=key_month, value=val_month, dict_source=data_selected_year)
        last_key = list(enumerate(data_columns))[len(data_columns)-1][1] # '31'
        if data_columns[last_key][0] == 'none':
            data_columns.pop(last_key)
        return data_columns
    elif mode =='c':
        calendar = read_csv(FILE_CALENDAR, splitter=';')
        calendar_selected_year = select(key=key_year, value=val_year, dict_source=calendar)
        calendar_selected_month = select(key=key_month, value=val_month, dict_source=calendar_selected_year)
        config = Config(calendar_selected_month)
        calendar = config.get_calendar()
        return calendar

class Config:
    def __init__(self, calendar, team=None, max_id=None):
        self.data_config = {'columns_static': {'fio': ['team', 'fio'], 'dep': ['team', 'dep'], 'grey': ['team', 'grey'], 'year': ['calendar', 'Year'], 'month': ['calendar', 'Month_Ru']},
                       'dict_mapping': {'team': team, 'calendar': calendar},
                       'titles_static': ['ФИО', 'Направление', 'Старший', 'Год', 'Месяц'],
                       'columns_dynamic': {'header': ['calendar', 'Day'], 'content': ['calendar', 'Holiday'],'weekday':['calendar','Day_Ru']}
                       }
        self.id_key = 'id'
        if max_id == None:
            self.id = 0
        else:
            self.id = int(max_id)
        self.columns_static_key = list(self.data_config.keys())[0]  #-->columns_static
        self.dict_mapping_key = list(self.data_config.keys())[1]  #-->dict_mapping
        self.columns_dynamic_key = list(self.data_config.keys())[3]  # -->columns_dynamic
        self.calendar = calendar
        if team != None:
            self.team = team

    def get_item(self,config,key,mode='dict'):
        if mode == 'dict':
            return (item for item in config[key].items())
    def set_id(self):
        self.id += 1

    def get_id(self):
        return  self.id

    def get_columns(self,mode='data'):
        data_columns = {}
        #create id key in dict data_columns
        data_columns[self.id_key] = []
        #create static  keys in dict data_columns
        for item in self.get_item(self.data_config, self.columns_static_key, mode='dict'):
            #-->item = ('fio', ['team', 'fio'])
            data_columns[item[0]] = []
        flag = 1
        header = self.data_config[self.columns_dynamic_key]['header'][1] #-->'columns_dynamic': {'header': ['calendar', 'Day']}         -->  'Day'
        content = self.data_config[self.columns_dynamic_key]['content'][1] #-->'columns_dynamic':{'content': ['calendar', 'Holiday']}   -->  'Holiday'
        team_fio = self.data_config[self.columns_static_key]['fio'][1] #-->'columns_static': {'fio': ['team', 'fio']}                   -->  'fio'
        for i in range(len(self.calendar[header])): #iteration on days, like 1,2,3...31
            # create dynamic columns (keys)
            data_columns[self.calendar[header][i]] = []  # add key Day like '1':[], ... '31':[]
            if mode == 'data':
                for j in range(len(self.team[team_fio])): #iteration on fio-items, like Ivanov, Petrov...
                    if flag == 1:
                        self.set_id() #will increase id+1
                        data_columns[self.id_key].append(self.get_id()) #fill up id-column, i.e. data_columns = {'id':[+id_current]}
                        #create static outter columns
                        for item in self.get_item(self.data_config, self.columns_static_key, mode='dict'): #-->{'fio': ['team', 'fio'], 'dep': ['team', 'dep'], 'grey': ['team', 'grey'], 'year': ['calendar', 'Year'], 'month': ['calendar', 'Month_Ru']}
                            #-->item = ('fio', ['team', 'fio'])
                            field = item[0]  # 'fio'
                            source_name = item[1][0]  # 'team'
                            source_dict = self.data_config[self.dict_mapping_key][source_name] #-->'dict_mapping': {'team': team} --> team
                            if source_dict == self.calendar:
                                it = i
                            else:
                                 it = j
                            source_field = item[1][1]  # 'fio' -field in source_dict
                            data_columns[field].append(source_dict[source_field][it]) #--> data_columns = {'fio':[+Ivanov], 'year':[+2018]....} here fill up static columns
                        data_columns[self.calendar[header][i]].append(self.calendar[content][i]) #--> data_columns ={'1':[+'y']}
                    else:
                        data_columns[self.calendar[header][i]].append(self.calendar[content][i]) #--> data_columns ={'1':[+'y']}
                flag = 0
        return data_columns

    def get_calendar(self):
        calendar = {}
        for key, val  in self.data_config[self.columns_dynamic_key].items(): #-->{'header': ['calendar', 'Day'], 'content': ['calendar', 'Holiday'],'weekday':['calendar','Day_Ru']}
            calendar[key] = self.calendar[val[1]]
        return calendar


 #----------------------------------Const---------------------------------------------------------------
DATA_DIR = join(dirname(__file__), 'static/csv')  # file = r'C:\folder\myfile.csv' - еще один способ
FILE_TEAM = join(DATA_DIR, 'team.csv')
FILE_CALENDAR = join(DATA_DIR, 'calendar.csv')
FILE_DATA = join(DATA_DIR, 'data.csv')

if __name__ == '__main__':
    #>--------------------------------Create team----------------------------------------------------------
    raw_data= get_team()
    raw_header = [key for key in raw_data ]
    #>--------------------------------Write team-----------------------------------------------------------
    write_csv(FILE_TEAM, raw_data, raw_header)
    # >--------------------------------Read team-----------------------------------------------------------
    team = read_csv(FILE_TEAM)
    #>--------------------------------Read calendar--------------------------------------------------------
    calendar = read_csv(FILE_CALENDAR, splitter=';')
    #>-------------------------------Create data----------------------------------------------------------
    mode = 'w'
    year = '2018'
    month = 'Июль'
    header, data_columns, check =  get_params(mode=mode,calendar=calendar, team=team, val_month=month)
   #>-------------------------------Write data ----------------------------------------------------------
    write_csv(file=FILE_DATA,data=data_columns,header = header, mode=mode,check=check)
    #sys.exit()
    # >-------------------------------Read data -----------------------------------------------------------
    mode = 'r'
    month = 'Июль'
    data_columns = get_params(mode=mode, key_year='year', val_year='2018', key_month='month', val_month=month)
    sys.exit()
    #>-------------------------------Show data ------------------------------------------------------------
    source = ColumnDataSource(data_columns)
    width_dict = {'fio': 200, 'dep': 80, 'grey': None, 'year': 0, 'month': 0}
    columns_width = {}
    for key in data_columns:
        if key in width_dict:
            columns_width[key] = width_dict[key]
        else:
            columns_width[key] = 36
    columns = [TableColumn(field=key, title=key, width=columns_width[key]) for key in data_columns ]
    data_table = DataTable(source=source, columns=columns,width=1500,fit_columns=True, editable=True)
    show(data_table)










