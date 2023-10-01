import pyodbc
import configparser

config = configparser.ConfigParser()

config_data = configparser.ConfigParser()
config_data.read("Tool Room Inventory.ini")

trInventory = config_data["Tool Room Inventory"]

# Define the connection parameters
driver = trInventory.get('driver')
server = trInventory.get('server')
database = trInventory.get('database')
username = trInventory.get('username')
password = trInventory.get('password')

db_name = trInventory.get('db_name')

# Create a connection string
conn_str = ("DRIVER=" + driver
            + ";SERVER=" + server
            + ";DATABASE=" + database
            + ";UID=" + username
            + ";PWD=" + password
            + ";TrustServerCertificate=yes")

try:
    # Connect to the SQL Server instance
    conn = pyodbc.connect(conn_str, autocommit=True)
    cursor = conn.cursor()

    # Define the SQL command to create the database
    create_db_sql = f"CREATE DATABASE {db_name}"

    # Execute the SQL command to create the database
    cursor.execute(create_db_sql)

    print(f"Database '{db_name}' created successfully.")

except pyodbc.Error as e:
    print(f"{e}")

