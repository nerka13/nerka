from flask import Flask
from flask import render_template
from flask import jsonify, request
import json
from tool import FILE_DATA
from model import make_components,make_calendar,find_save
import datetime

app = Flask(__name__)

@app.route('/')
def show_proba():
    columns, data = make_components(val_year = year, val_month= month)
    columns= json.dumps(columns)
    data = json.dumps(data)
    return render_template('main.html',columns=columns, data=data)

@app.route('/table', methods=['POST'])
def pass_table():
    browser = request.form
    if browser['month'] == 'previous':
        if now.month == 1:
            month = 'Декабрь'
            year = str(now.year-1)
        else:
            month = month_name[str(now.month-1)]
            year = str(now.year)
    elif browser['month'] == 'current':
        month = month_name[str(now.month)]
        year = str(now.year)
    else:
        if now.month == 12:
            month = 'Январь'
            year = str(now.year+1)
        else:
            month = month_name[str(now.month+1)]
            year = str(now.year)
    global calendar
    calendar = make_calendar(val_year=year, val_month=month)
    columns, data = make_components(val_year = year, val_month= month)
    columns = json.dumps(columns)
    data = json.dumps(data)
    return jsonify(columns=columns, data=data)

@app.route('/data', methods=['POST'])
def pass_data():
    browser = request.form
    browsered = {}
    browsered.update(browser)
    new_val = find_save(id=browsered['id'][0],key=browsered['key'][0],new_val=browsered['newVal'][0],calendar=calendar,file=file)
    return jsonify(new_val)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

if __name__ == '__main__':
    month_name = {'1':'Январь','2':'Февраль','3':'Март','4':'Апрель','5':'Май','6':'Июнь','7':'Июль','8':'Август','9':'Сентябрь','10':'Октябрь','11':'Ноябрь','12':'Декабрь'}
    #delta = datetime.timedelta(days=150)
    #now = datetime.datetime.now() #+ delta
    now = datetime.date(2018, 8, 1)
    print(now)
    file = FILE_DATA
    year = str(now.year)
    month = month_name[str(now.month)]
    calendar = make_calendar(val_year=year, val_month=month)
    app.run(port=5003, debug=True)

