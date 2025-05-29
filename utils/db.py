import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

# Create SQLAlchemy engine for pandas
def get_engine():
    return create_engine("mysql+mysqlconnector://root:root@localhost/smart_classroom")

# Create connection for manual SQL operations (inserts)
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="smart_classroom"
    )

def insert_attendance(name, timestamp):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance WHERE name=%s AND DATE(timestamp)=CURDATE()", (name,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO attendance (name, timestamp) VALUES (%s, %s)", (name, timestamp))
        conn.commit()
    cursor.close()
    conn.close()

def insert_attention(name, timestamp, attentive):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO attention (name, timestamp, attentive) VALUES (%s, %s, %s)",
                   (name, timestamp, attentive))
    conn.commit()
    cursor.close()
    conn.close()

def get_attendance_data():
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM attendance", engine)
    return df

def get_attention_data():
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM attention", engine)
    return df
