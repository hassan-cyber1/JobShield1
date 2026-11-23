
import sqlite3

DATABASE = "jobs.db"


def connect_db():
    return sqlite3.connect(DATABASE)


def init_db():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS advertisements (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            job_title TEXT NOT NULL,

            company_name TEXT NOT NULL,

            advertisement_text TEXT NOT NULL,

            risk_score INTEGER NOT NULL,

            risk_level TEXT NOT NULL,

            detected_warnings TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    conn.commit()
    conn.close()


def save_analysis(job_title, company_name, job_text,
                  score, risk, warnings):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO advertisements
        (job_title, company_name, advertisement_text,
         risk_score, risk_level, detected_warnings)

        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        job_title,
        company_name,
        job_text,
        score,
        risk,
        ", ".join(warnings)
    ))

    conn.commit()
    conn.close()


def get_history():

    conn = connect_db()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM advertisements
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    conn.close()

    return records
def save_contact(name, email, message):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        INSERT INTO contact_messages (name, email, message)
        VALUES (?, ?, ?)
    """, (name, email, message))

    conn.commit()
    conn.close()