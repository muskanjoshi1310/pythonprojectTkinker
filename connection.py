pip install mysql-connector-python

import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",       # Your MySQL server address
        user="root",            # Your MySQL username
        password="password",    # Your MySQL password
        database="library_system" # Your MySQL database name
    )
