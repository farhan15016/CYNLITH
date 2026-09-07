import json
from dataclasses import dataclass

from ai.cynthia import ask_cynthia


@dataclass
class StudySession:
    subject: str
    topic: str
    level: str
    mode: str = "STANDARD"

    def generate_lesson(self) -> dict:
        prompt = f"""
You are Cynthia, an expert AI learning companion.

Create a structured lesson for a learner.

Subject: {self.subject}
Topic: {self.topic}
Learner level: {self.level}
Teaching mode: {self.mode}

Your goal is to teach the topic clearly and progressively.

Return ONLY valid JSON.
Do not use Markdown code fences.
Do not add any text before or after the JSON.

Use exactly this structure:

{{
  "title": "Lesson title",
  "core_idea": "The most important idea the learner should understand.",
  "explanation": "A clear explanation adapted to the learner's level.",
  "example": "A simple and useful example.",
  "visual": {{
    "needed": true,
    "type": "diagram",
    "description": "Describe a useful visual that would help explain the concept."
  }},
  "video": {{
    "needed": true,
    "topic": "Describe what an educational video should explain."
  }},
  "quick_check": "One short question that checks understanding."
}}

Rules:
- Keep the explanation clear and educational.
- Start with the fundamental concept.
- Use an example that makes the idea easier to understand.
- Set visual.needed to true only when a visual would genuinely improve understanding.
- Set video.needed to true only when a video would genuinely improve understanding.
- The visual description must describe the educational purpose of the visual.
- The video topic must describe what the video should teach.
- The quick check must not include its answer.
"""

        response = ask_cynthia(prompt)

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "title": self.topic,
                "core_idea": response,
                "explanation": "",
                "example": "",
                "visual": {
                    "needed": False,
                    "type": "",
                    "description": "",
                },
                "video": {
                    "needed": False,
                    "topic": "",
                },
                "quick_check": "",
            }

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
