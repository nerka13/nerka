from tool import get_params, read_csv, write_csv
import pandas as pd
import sys
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from tool import FILE_DATA, FILE_TEAM, FILE_CALENDAR
from flask import Flask
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

app = Flask(__name__)

def make_data(val_year,val_month):
    data = get_params(mode='r', key_year='year', val_year=val_year, key_month='month', val_month=val_month)
    return data

def column_grid(field,name=None,id=None,width=35):
    if name == None:
        name = field
    if id == None:
        id = field
    ret = {'id': id, 'name': name, 'field': field, 'width':width }
    return ret

def data_grid(data,columns):
    records = []
    length = len(data[list(data.keys())[0]])
    for i in range(length):
        record = {}
        for item in columns:
            key = item['field']
            record[key] = data[key][i]
        records.append(record)
    return records

def make_components(val_year, val_month):
    try:
        data = make_data(val_year, val_month)
    except:
        print('EXCEPTION')
        # >--------------------------------Read team-----------------------------------------------------------
        team = read_csv(FILE_TEAM)
        # >--------------------------------Read calendar--------------------------------------------------------
        calendar = read_csv(FILE_CALENDAR, splitter=';')
        # >-------------------------------Create data----------------------------------------------------------
        header, data_columns, check = get_params(mode='a', calendar=calendar, team=team, val_year=val_year, val_month=val_month)
        # >-------------------------------Write data ----------------------------------------------------------
        write_csv(file=FILE_DATA, data=data_columns, header=header, mode='a', check=check)
        data = make_data(val_year, val_month)

    params = {'width':{'id':40,'fio': 290, 'dep': 155,'year':45,'month':80},
              'name_field': {'id': 'Id', 'fio': 'ФИО', 'dep': 'Департамент', 'year': 'Год', 'month': 'Месяц'}
             }
    columns = []
    for key in data:
        if key in list(params['width'].keys()):
            width = params['width'][key]
            name_field = params['name_field'][key]
            columns.append(column_grid(field=key,width=width,name=name_field))
        else:
            columns.append(column_grid(field=key, width=30))
    rows = data_grid(data, columns)
    return columns, rows

def make_calendar(val_year,val_month):
    calendar = get_params(mode='c', val_year=val_year, val_month=val_month)
    return calendar

def find_save(id,key,new_val,calendar,file):
    if new_val == 'd': #delete - it's initial value
        idx = calendar['header'].index(key)
        val = calendar['content'][idx]
        new_val = val
    df = pd.read_csv(file, encoding='cp1251', keep_default_na=False)
    df.loc[lambda df: df.id == int(id), key] = new_val
    df.to_csv(file, index=False)
    return new_val


if __name__ == '__main__':
    id = 'id'
    file = FILE_DATA
    year_req = '2018'
    month_req = 'Май'
    columns, data = make_components(val_year=year_req, val_month=month_req)
    print('data', data)
    print('columns', columns)





