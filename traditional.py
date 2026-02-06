import pymysql
from dotenv import load_dotenv

load_dotenv()

import os
while True:

    try:
        conn=pymysql.connect(database=os.getenv("DB_NAME"),user=os.getenv("DB_USER"),password=os.getenv("DB_PASSWORD"),port=os.getenv("DB_PORT"),host=os.getenv("DB_HOST"))
        cursor=conn.cursor()
        print("DATABASE CONNECTION SUCESSFUL")
        cursor.execute(""" CREATE TABLE IF NOT EXISTS members ( id INT AUTO_INCREMENT PRIMARY KEY, firstname VARCHAR(50), lastname VARCHAR(50), email VARCHAR(100), role VARCHAR(50) ) """)
        conn.commit()
        break

    except Exception as error:
        print("Database Connection Failed")
        print(f"Error:{error}")
