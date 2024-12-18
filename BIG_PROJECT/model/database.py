# model/database.py

import sqlite3


def init_db():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            student_id TEXT,
            date_of_birth TEXT,
            barcode TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_student_info(student_info):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    name = student_info.get('name', "Không xác định")
    student_id = student_info.get('student_id', "Không xác định")
    date_of_birth = student_info.get('date_of_birth', "Không xác định")
    barcode = student_info['barcode'][0]['data'] if student_info.get('barcode') else ""

    cursor.execute('''
        INSERT INTO students (name, student_id, date_of_birth, barcode)
        VALUES (?, ?, ?, ?)
    ''', (name, student_id, date_of_birth, barcode))

    conn.commit()
    conn.close()
