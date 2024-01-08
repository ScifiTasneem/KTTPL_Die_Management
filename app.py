import webbrowser
import pandas as pd
from die_dictionary_uniquecode import dieDict, dieNo
from flask import Flask, render_template, request, redirect, url_for, flash
from wtforms import StringField, validators, Form
import configparser
import pyodbc
import datetime

global dieList

app = Flask(__name__)
app.secret_key = 'you_will_never_guess'

config_data = configparser.ConfigParser()
config_data.read('Tool Room Inventory.ini')
trInventory = config_data['Tool Room Inventory']

driver = trInventory.get('driver')
server = trInventory.get('server')
database = trInventory.get('db_name')
username = trInventory.get('username')
password = trInventory.get('password')

# Create a connection string
conn_str = ("DRIVER=" + driver
            + ";SERVER=" + server
            + ";DATABASE=" + database
            + ";UID=" + username
            + ";PWD=" + password
            + ";TrustServerCertificate=yes")

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    print('Connection established successfully')
except pyodbc.Error as e:
    print(f'Error: {e}')


class DieForm(Form):
    unique_code = StringField('Unique Code', [
        validators.InputRequired(message='Unique code is required.'),
        validators.Length(min=5, max=5, message='Unique code should be 5 digits.'),
        validators.Regexp('^[0-9]{5}$', message='Unique code should only contain numbers in the format 00001-99999.')
    ])


@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(username, password)
        if username == 'admin' and password == 'ktfl@123':
            return redirect(url_for('upload'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    global dieList

    dieList = set()

    if request.method == 'POST':
        file = request.files['file']
        dieExcel = pd.read_excel(file)

        try:
            for die in dieExcel['Die No']:
                die = str(die)
                for actualDie in dieNo:
                    if die == actualDie:
                        dieList.add(die)
        except KeyError:
            flash('Data not submitted in proper format')

        for x in dieList:
            print(f'Set {x}')
        return redirect(url_for('die_form'))
    return render_template('upload_excel.html')


def create_table():
    try:
        for die in dieList:
            create_die_sql = f"""
                           IF NOT EXISTS (SELECT * FROM sys.tables WHERE name= 'DIE_NO{die}')
                           BEGIN
                                CREATE TABLE DIE_NO{die}
                                (
                                UNIQUE_CODE VARCHAR(10) PRIMARY KEY,
                                ELEMENT VARCHAR(20),
                                CONDITION VARCHAR(20)                    
                                )
                           END
                           """
            cursor.execute(create_die_sql).commit()

    except KeyError:
        return redirect(url_for('upload'))


def insert_values():
    global dieList

    for die in dieList:
        check_query = f'SELECT UNIQUE_CODE FROM DIE_NO{die}'
        result = cursor.execute(check_query).fetchone()

        if result is None:
            try:
                die = str(die)
                for key, value in dieDict.items():
                    if die == value[0]:
                        try:
                            insert_query = f"INSERT INTO DIE_NO{die} (UNIQUE_CODE, ELEMENT) VALUES (?,?)"
                            values = key, value[1]
                            cursor.execute(insert_query, values).commit()
                        except pyodbc.Error:
                            pass
                    else:
                        pass
            except KeyError:
                return redirect(url_for('upload'))
        else:
            pass


@app.route('/die_form', methods=['POST', 'GET'])
def die_form():
    create_table()
    insert_values()

    global dieList
    form = DieForm(request.form)

    if request.method == 'POST' and form.validate():
        unique_code = form.unique_code.data
        die_condition = request.form.get('die_details')
        condition_data = die_condition
        print(die_condition, unique_code)

        conditionDict = {'1': 'Welding', '2': 'GR', '3': 'Sinking Vendor', '4': 'Sinking Inhouse',
                         '5': 'Polishing', '6': 'Vent Holes', '7': 'Inspection', '8': 'Nitriding', '9': 'Readiness',
                         '10': 'Production', '11': 'Unavailable'}

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        stageData = conditionDict.get(condition_data)
        stageValues = current_time, unique_code, stageData

        form_data_query = 'INSERT INTO DIE_TRACE (TIME_STAMP, UNIQUE_CODE, STAGE) VALUES (?,?,?)'
        cursor.execute(form_data_query, stageValues).commit()

        if die_condition in ['1', '2', '3', '4', '5', '6', '7', '8']:
            die_condition = 'Under Repair'
        elif die_condition in ['9', '10']:
            die_condition = 'Ready'
        elif die_condition == '11':
            die_condition = 'Production'
        elif die_condition == '12':
            die_condition = 'Unavailable'

        value = dieDict.get(unique_code)
        print(die_condition, value)

        form_insert_query = f"UPDATE DIE_NO{value[0]} SET CONDITION='{die_condition}' " \
                            f"WHERE ELEMENT='{value[1]}' AND UNIQUE_CODE={unique_code}"
        cursor.execute(form_insert_query).commit()

        return redirect(url_for('dashboard'))
    return render_template('die_form.html', form=form)


@app.route('/dashboard')
def dashboard():
    global dieList

    elementList = ['UPT', 'UPB', 'BLT', 'BLB', 'FIT', 'FIB', 'TRD', 'TRP', 'PRP', 'PDT', 'PDB', 'STP']
    conditionList = ['Ready', 'Under Repair', 'Unavailable', 'Production']

    data = []

    for die in dieList:
        for element in elementList:
            element_data = {'Die': die, 'Element': element, 'Conditions': {}}
            for condition in conditionList:
                query = f"SELECT COUNT(CONDITION) FROM DIE_NO{die} WHERE ELEMENT='{element}' AND CONDITION='{condition}'"
                result = cursor.execute(query).fetchval()
                element_data['Conditions'][condition] = result
            data.append(element_data)

    return render_template('dashboard.html', data=data)


@app.route('/hatebur_form')
def hatebur_form():
    form = DieForm(request.form)

    return render_template('hatebur_form.html', form=form)


if __name__ == '__main__':
    webbrowser.open_new_tab('http://127.0.0.1:5010')
    app.run(debug=True, use_reloader=False, port=5010)
