from dataclasses import dataclass
from ai.cynthia import ask_cynthia


@dataclass
class StudySession:
    subject: str
    topic: str
    level: str
    mode: str = "STANDARD"

    def generate_lesson(self) -> str:
        prompt = f"""
You are starting a study session.

Subject: {self.subject}
Topic: {self.topic}
Learner level: {self.level}
Teaching mode: {self.mode}

Teach this topic as the first lesson of the study session.

Start with the core idea, then explain how it works and give a simple example.
Adapt the explanation to the learner's level and teaching mode.
Do not assume the learner already understands advanced concepts.
End with one short question to check their understanding.
"""

        return ask_cynthia(prompt)
