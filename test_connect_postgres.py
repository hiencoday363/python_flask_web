from sqlalchemy import create_engine

server = 'database-postgres-1.cidw3wkwqevk.us-east-1.rds.amazonaws.com' # to specify an alternate port
database = 'flask' 
username = 'sa' 
password = 'hien0362363616'
port = 5432

engine = create_engine(f'postgresql://{username}:{password}@{server}:{port}/{database}')

conn = engine.connect()
print('connected')

rows = conn.execute("SELECT * FROM login_dk ")
# 
data = rows.fetchall() 

print(data)
