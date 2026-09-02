import sqlite3

DB_NAME = "backend/cynlith.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_message(role: str, content: str):
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        "INSERT INTO messages (role, content) VALUES (?, ?)",
        (role, content),
    )
    conn.commit()
    conn.close()


def get_messages():
    conn = sqlite3.connect(DB_NAME)
    rows = conn.execute(
        "SELECT role, content FROM messages ORDER BY id"
    ).fetchall()
    conn.close()

    return [
        {"role": role, "content": content}
        for role, content in rows
    ]
