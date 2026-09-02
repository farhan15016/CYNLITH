from dataclasses import dataclass
from ai.cynthia import ask_cynthia


@dataclass
class Assessment:
    subject: str
    topic: str
    level: str
    mode: str = "STANDARD"

    def generate_question(self) -> str:
        prompt = f"""
Create one assessment question for a learner.

Subject: {self.subject}
Topic: {self.topic}
Learner level: {self.level}
Teaching mode: {self.mode}

The question should test genuine understanding of the topic.
Match the difficulty to the learner's level and teaching mode.
Do not provide the answer.
Return only the question.
"""

        return ask_cynthia(prompt)
    def evaluate_answer(self, question: str, answer: str) -> str:
        prompt = f"""
Evaluate the learner's answer to an assessment question.

Subject: {self.subject}
Topic: {self.topic}
Learner level: {self.level}
Teaching mode: {self.mode}

Question:
{question}

Learner's answer:
{answer}

Evaluate whether the answer is correct, partially correct, or incorrect.
Explain briefly why.
If the answer is incorrect or incomplete, give a short hint rather than simply giving the full answer.

Return the evaluation in this format:

Result: Correct / Partially Correct / Incorrect
Feedback: ...
Hint: ...
"""

        return ask_cynthia(prompt)
