import sqlite3
from dataclasses import dataclass


DB_NAME = "backend/cynlith.db"


def init_progress_db():
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS learning_progress (
            subject TEXT NOT NULL,
            topic TEXT NOT NULL,
            attempts INTEGER NOT NULL DEFAULT 0,
            correct INTEGER NOT NULL DEFAULT 0,
            partially_correct INTEGER NOT NULL DEFAULT 0,
            incorrect INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (subject, topic)
        )
    """)

    conn.commit()
    conn.close()


@dataclass
class LearningProgress:
    subject: str
    topic: str
    attempts: int = 0
    correct: int = 0
    partially_correct: int = 0
    incorrect: int = 0

    def __post_init__(self):
        init_progress_db()

        conn = sqlite3.connect(DB_NAME)

        row = conn.execute(
            """
            SELECT attempts, correct, partially_correct, incorrect
            FROM learning_progress
            WHERE subject = ? AND topic = ?
            """,
            (self.subject, self.topic)
        ).fetchone()

        conn.close()

        if row:
            (
                self.attempts,
                self.correct,
                self.partially_correct,
                self.incorrect,
            ) = row

    def save(self):
        conn = sqlite3.connect(DB_NAME)

        conn.execute(
            """
            INSERT INTO learning_progress
                (subject, topic, attempts, correct, partially_correct, incorrect)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(subject, topic)
            DO UPDATE SET
                attempts = excluded.attempts,
                correct = excluded.correct,
                partially_correct = excluded.partially_correct,
                incorrect = excluded.incorrect
            """,
            (
                self.subject,
                self.topic,
                self.attempts,
                self.correct,
                self.partially_correct,
                self.incorrect,
            )
        )

        conn.commit()
        conn.close()

    def record_result(self, result: str):
        self.attempts += 1

        result = result.lower()

        if "partially correct" in result:
            self.partially_correct += 1
        elif "incorrect" in result:
            self.incorrect += 1
        elif "correct" in result:
            self.correct += 1

        self.save()

    def get_status(self) -> str:
        if self.attempts == 0:
            return "Not Started"

        accuracy = self.correct / self.attempts

        if accuracy < 0.5:
            return "Needs Review"
        elif accuracy < 0.8:
            return "Improving"
        else:
            return "Strong"

    def get_next_action(self) -> str:
        status = self.get_status()

        if status == "Needs Review":
            return "Review the concept with a simpler explanation."

        elif status == "Improving":
            return "Continue practicing with another question."

        elif status == "Strong":
            return "Increase the difficulty of the next question."

        return "Start learning the topic."

    def to_dict(self):
        return {
            "subject": self.subject,
            "topic": self.topic,
            "attempts": self.attempts,
            "correct": self.correct,
            "partially_correct": self.partially_correct,
            "incorrect": self.incorrect,
        }
