import pyodbc
import configparser

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

    create_table_sql = """
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'DTR_INVENTORY')
    BEGIN
        CREATE TABLE DTR_INVENTORY (
        UNIQUE_CODE VARCHAR(10),
        CONDITION VARCHAR(50)
        )
    END
    """
    cursor.execute(create_table_sql)
    conn.commit()
    conn.close()
except pyodbc.Error as e:
    print(f"Error:{e}")

