import pyodbc


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