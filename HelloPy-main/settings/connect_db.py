import psycopg2
import os
from azure.identity import ManagedIdentityCredential,DefaultAzureCredential,AzureCliCredential

host = os.environ.get("DBHOST")
dbname = os.environ.get("DBNAME")
user = os.environ.get("DBUSER")
password = os.environ.get("DBPASSWORD")


def connect():
    credential = ManagedIdentityCredential(client_id=os.environ.get("AZURE_CLIENT_ID"))
    token = credential.get_token("https://ossrdbms-aad.database.windows.net/.default")
    print(f"generated token is {token}")
    conn_string = "host={0} user={1} dbname={2} password={3}".format(host, user, dbname, token.token)
    conn = psycopg2.connect(conn_string) 
    cursor = conn.cursor()
    return [conn,cursor]


def fetchData():
    connectors = connect()
    conn,cursor = connectors[0],connectors[1]
    postgreSQL_select_Query = "select * from users"
    cursor.execute(postgreSQL_select_Query)
    publisher_records = cursor.fetchall()
    users = []
    for row in publisher_records:
        ls = [row[1],row[2]]
        users.append(ls)
    conn.close()
    cursor.close()
    
    return users
    


def saveData(name,email):
    connectors = connect()
    conn,cursor = connectors[0],connectors[1]
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s);", (name, email))
    print("data saved!")
    conn.commit()
    cursor.close()
    conn.close()

def createDB():
    connectors = connect()
    conn,cursor = connectors[0],connectors[1]
    cursor.execute("CREATE TABLE users (id serial PRIMARY KEY, name VARCHAR(50), email VARCHAR(50));")
    conn.commit()
    cursor.close()
    conn.close()
'''


conn_string = "host={0} user={1} dbname={2} password={3}".format(host, user, dbname, password)
print(f"connection string {conn_string}")
conn = psycopg2.connect(conn_string) 
print("Connection established")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS inventory;")
print("Finished dropping table (if existed)")

cursor.execute("CREATE TABLE users (id serial PRIMARY KEY, name VARCHAR(50), email VARCHAR(50);")
print("Finished creating table")

cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("banana", 150))
cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("orange", 154))
cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("apple", 100))
print("Inserted 3 rows of data")

conn.commit()
cursor.close()
conn.close()'''
