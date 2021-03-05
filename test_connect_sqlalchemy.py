#config
'''
conn = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=DESKTOP-G2RKN51\\SQLEXPRESS;'
    'Username=sa;'
    'Password=hien123;'
    'Database=flask;'
    'Trusted_Connection=true;'
)
'''


'''import pyodbc

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
'''

# import urllib
from sqlalchemy import create_engine

server = 'DESKTOP-G2RKN51\\SQLEXPRESS' # to specify an alternate port
database = 'flask' 
username = 'sa' 
password = 'hien123'
driver = 'SQL Server'

engine = create_engine(f"mssql://{username}:{password}@{server}/{database}?driver={driver}")

conn = engine.connect()
print('connected')

# title = "POST ABOUT CAR 1 test sqlalchemy"

#update
# update = conn.execute('UPDATE article SET title = ? WHERE ID = 1',title)

#insert
# insert = conn.execute("INSERT INTO article(title,content,img) VALUES ('test insert using sqlalchemy 1','Donec eget ex magna.','https://storage.googleapis.com/f1-cms/2020/04/3705bffc-20200428_090510.jpg')" )

# print('insert success')
#delete
# delete = conn.execute("DELETE FROM article WHERE ID > 15")

rows = conn.execute("SELECT * FROM login_dk WHERE email = ? ",'test@test.com')

data = rows.fetchall() 

# rows = conn.execute('UPDATE article SET title = ?',title)

print(len(data))
print(data[0][0])

# for i, row in enumerate(rows):
# 	if i == 0:
# 		print(row[0])



conn.close()