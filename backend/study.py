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
You are Cynthia, the AI learning companion inside Cynlith.

You are creating a personalized lesson for a learner.

Subject: {self.subject}
Topic: {self.topic}
Learner level: {self.level}
Teaching mode: {self.mode}

Create a clear, structured lesson.

The lesson must contain these sections:

1. core_idea
- Explain the central idea in a simple and accurate way.
- Keep it appropriate for the learner's level.

2. explanation
- Explain how the concept works.
- Use reasoning, steps, relationships, or mechanisms where appropriate.

3. example
- Give one useful real-world or practical example.

4. visual
Create a structured visual-learning description.

The visual object MUST contain:

- needed: true or false
- type: one of "diagram", "flowchart", "comparison", "timeline", "formula", "process", or "none"
- title: short title for the visual
- description: explain what the learner should see
- equation: an important equation if one exists, otherwise ""
- labels: an array of short labels
- relationships: an array describing how the labels/concepts connect

The visual should help the learner understand the concept rather than simply decorate the lesson.

Examples:

For Physics:
labels could be ["Force", "Mass", "Acceleration"]
relationships could be ["Force causes acceleration", "More mass requires more force"]

For Electronics:
labels could be ["Voltage", "Resistance", "Current"]
relationships could be ["Voltage drives current", "Resistance limits current"]

For Biology:
labels could be ["DNA", "RNA", "Protein"]
relationships could be ["DNA stores information", "RNA carries information", "RNA helps produce proteins"]

For Mathematics:
labels could describe the important quantities or steps.

For Programming:
labels could represent classes, objects, methods, inputs, outputs, or other important concepts.

5. video
Provide a short recommendation describing what kind of educational video would reinforce the concept.

6. quick_check
Create one short question that checks whether the learner understood the lesson.
Do not provide the answer.

IMPORTANT:
- Return ONLY valid JSON.
- Do not use Markdown.
- Do not put the JSON inside ``` fences.
- Do not add commentary before or after the JSON.

Use exactly this structure:

{{
  "core_idea": "...",
  "explanation": "...",
  "example": "...",
  "visual": {{
    "needed": true,
    "type": "diagram",
    "title": "...",
    "description": "...",
    "equation": "...",
    "labels": ["...", "...", "..."],
    "relationships": ["...", "..."]
  }},
  "video": {{
    "needed": true,
    "description": "..."
  }},
  "quick_check": "..."
}}
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
