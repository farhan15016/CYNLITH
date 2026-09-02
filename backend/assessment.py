from dataclasses import dataclass

from ai.cynthia import ask_cynthia


@dataclass
class Assessment:
    subject: str
    topic: str
    level: str
    mode: str = "STANDARD"

    def generate_question(self, difficulty: str | None = None) -> str:
        difficulty = difficulty or self.level

        prompt = f"""
Create one assessment question for a learner.

Subject: {self.subject}
Topic: {self.topic}
Learner level: {self.level}
Question difficulty: {difficulty}
Teaching mode: {self.mode}

The question should:
- Test genuine understanding of the topic.
- Match the specified difficulty level.
- Be appropriate for the learner's level and teaching mode.
- Require the learner to think rather than simply recall a definition.
- Be clear and unambiguous.

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
