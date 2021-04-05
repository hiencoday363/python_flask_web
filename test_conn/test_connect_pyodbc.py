import pyodbc

try:
	conn = pyodbc.connect(
	    'Driver={SQL Server};'
	    'Server=DESKTOP-G2RKN51\\SQLEXPRESS;'
	    'Username=sa;'
	    'Password=hien123;'
	    'Database=flask;'
	    'Trusted_Connection=true;'
	)
	print('connect')

	cursor = conn.cursor()
	cursor.execute("SELECT * FROM article")

	rows = cursor.fetchall()

	for i, row in enumerate(rows):
		if i == 0:
			print(row[0])
			
except:
	print('chua ket noi')

#config database sql server
'''
server = 'databasehienco.cidw3wkwqevk.us-east-1.rds.amazonaws.com,1433' # to specify an alternate port
database = 'flask' 
username = 'hien363' 
password = 'hien0362363616'
driver = 'SQL Server'
engine = create_engine(f"mssql+pymssql://{username}:{password}@{server}/{database}?driver={driver}")

'''