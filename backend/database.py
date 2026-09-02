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

    conn.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL,
            value TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS learner_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL UNIQUE,
            value TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS learner_subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL UNIQUE,
            level TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_message(role: str, content: str):
    conn = sqlite3.connect(DB_NAME)

    conn.execute(
        "INSERT INTO messages (role, content) VALUES (?, ?)",
        (role, content)
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


def save_memory(key: str, value: str):
    conn = sqlite3.connect(DB_NAME)

    conn.execute(
        "INSERT INTO memories (key, value) VALUES (?, ?)",
        (key, value)
    )

    conn.commit()
    conn.close()


def get_memories():
    conn = sqlite3.connect(DB_NAME)

    rows = conn.execute(
        "SELECT key, value FROM memories ORDER BY id"
    ).fetchall()

    conn.close()

    return [
        {"key": key, "value": value}
        for key, value in rows
    ]


def save_profile(key: str, value: str):
    conn = sqlite3.connect(DB_NAME)

    conn.execute(
        """
        INSERT INTO learner_profile (key, value)
        VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """,
        (key, value)
    )

    conn.commit()
    conn.close()


def get_profile():
    conn = sqlite3.connect(DB_NAME)

    rows = conn.execute(
        "SELECT key, value FROM learner_profile ORDER BY id"
    ).fetchall()

    conn.close()

    return [
        {"key": key, "value": value}
        for key, value in rows
    ]


def save_subject(subject: str, level: str):
    conn = sqlite3.connect(DB_NAME)

    conn.execute(
        """
        INSERT INTO learner_subjects (subject, level)
        VALUES (?, ?)
        ON CONFLICT(subject) DO UPDATE SET level = excluded.level
        """,
        (subject, level)
    )

    conn.commit()
    conn.close()


def get_subjects():
    conn = sqlite3.connect(DB_NAME)

    rows = conn.execute(
        "SELECT subject, level FROM learner_subjects ORDER BY id"
    ).fetchall()

    conn.close()

    return [
        {"subject": subject, "level": level}
        for subject, level in rows
    ]
