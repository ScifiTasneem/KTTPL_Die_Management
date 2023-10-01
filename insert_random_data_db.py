import pyodbc
import configparser
import random

dieRequired = ['244', '644', '1619']
elementList = ['UPT', 'UPB', 'BLT', 'BLB', 'FIT', 'FIB', 'TRD', 'TRP', 'PRP', 'PDT', 'PDB', 'STP']
conditionList = ['Ready', 'Under Repair', 'Production']
config = configparser.ConfigParser()

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

    for die in dieRequired:
        for element in elementList:
            condition = random.choice(conditionList)
            query = f"UPDATE DIE_NO{die} SET CONDITION='{condition}' WHERE ELEMENT='{element}'"
            cursor.execute(query)

    conn.commit()
    print('Changes committed successfully')

except pyodbc.Error as e:
    print(f"Error: {e}")

finally:
    cursor.close()
    conn.close()
