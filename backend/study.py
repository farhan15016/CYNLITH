from dataclasses import dataclass


@dataclass
class StudySession:
    subject: str
    topic: str
    level: str
    mode: str = "STANDARD"
