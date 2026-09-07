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
    def generate_check_question(self) -> str:
        prompt = f"""
Create one short understanding-check question for a learner.

Subject: {self.subject}
Topic: {self.topic}
Learner level: {self.level}
Teaching mode: {self.mode}

The question should:
- Check whether the learner understood the lesson.
- Match the learner's level.
- Require a short explanation or reasoning.
- Be clear and unambiguous.
- Not require advanced knowledge beyond the topic.

Do not provide the answer.
Return only the question.
"""

        return ask_cynthia(prompt)
