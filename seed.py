# seed.py

import mysql.connector
import csv
import uuid
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Retrieve DB credentials securely
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


def connect_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.close()

def connect_to_prodev():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL
        )
    """)
    connection.commit()
    print("Table user_data created successfully")
    cursor.close()

def insert_data(connection, csv_file):
    cursor = connection.cursor()
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (str(uuid.uuid4()), row['name'], row['email'], int(row['age'])))
            except Exception as e:
                print("Insert error:", e)
    connection.commit()
    cursor.close()
