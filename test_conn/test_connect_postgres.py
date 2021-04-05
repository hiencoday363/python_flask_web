from sqlalchemy import create_engine

server = 'localhost' # to specify an alternate port
database = 'flask' 
username = 'postgres' 
password = ''
port = 5432
# server = 'database-postgres-1.cidw3wkwqevk.us-east-1.rds.amazonaws.com' # to specify an alternate port
# password = 'hien0362363616'
# username = 'sa' 

engine = create_engine(f'postgresql://{username}:{password}@{server}:{port}/{database}')

conn = engine.connect()
print('connected')

# rows = conn.execute("SELECT * FROM login_dk ")
# # 
# data = rows.fetchall() 

# print(data)
