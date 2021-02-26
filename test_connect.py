import pyodbc

server_name = "server=databasehienco.cidw3wkwqevk.us-east-1.rds.amazonaws.com,1433;"
user_name = "uid=hien363;"
password = "pwd=hien0362363616;"
db_name = "Database=flask;"
trusted = "Trusted_Connection=no;"

config = "Driver={SQL Server};" + server_name + user_name + password + db_name + trusted

try:
	conn = pyodbc.connect(config)
	print('connect')
except Exception as error:
	print(error)
