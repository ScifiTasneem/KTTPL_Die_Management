import configparser

config = configparser.ConfigParser()

config.add_section("Tool Room Inventory")

# Adding key-value pairs
config.set("Tool Room Inventory", "driver", "{ODBC Driver 17 for SQL Server}")
config.set("Tool Room Inventory", "server", "W3PIOT001\SQLEXPRESS")
config.set("Tool Room Inventory", "database", "master")
config.set("Tool Room Inventory", "username", "sa")
config.set("Tool Room Inventory", "password", "ktfl@123")
config.set("Tool Room Inventory", "db_name", "DIE_TOOL_ROOM")

with open("Tool Room Inventory.ini", 'w') as example:
    config.write(example)

config_data = configparser.ConfigParser()

config_data.read("Tool Room Inventory.ini")

database = config_data["Tool Room Inventory"]

print(database.get('server'))
