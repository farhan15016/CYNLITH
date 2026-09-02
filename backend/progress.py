from dataclasses import dataclass


@dataclass
class LearningProgress:
    subject: str
    topic: str
    attempts: int = 0
    correct: int = 0
    partially_correct: int = 0
    incorrect: int = 0

    def record_result(self, result: str):
        self.attempts += 1

        result = result.lower()

        if "partially correct" in result:
            self.partially_correct += 1
        elif "incorrect" in result:
            self.incorrect += 1
        elif "correct" in result:
            self.correct += 1
