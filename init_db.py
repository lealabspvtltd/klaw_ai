import sqlite3

def init_db():
    conn = sqlite3.connect('courses.db')
    cursor = conn.cursor()

    # Table for storing course metadata and syllabus
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_code TEXT NOT NULL UNIQUE,
            course_name TEXT,
            university TEXT,
            course_group TEXT,
            branch TEXT,
            semester TEXT,
            syllabus_text TEXT
        )
    ''')

    # Table for storing materials (linked to course)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_code TEXT,
            file_name TEXT,
            extracted_text TEXT,
            FOREIGN KEY(course_code) REFERENCES courses(course_code)
        )
    ''')

    conn.commit()
    conn.close()

# Run this to create the database before starting the app
if __name__ == '__main__':
    init_db()
