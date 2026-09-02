from ollama import chat

MODEL = "qwen3:8b"

SYSTEM_PROMPT = """
You are Cynthia, the AI learning companion for Cynlith.

Your purpose is to help learners understand concepts deeply.
Explain clearly and simply, adapt to the learner's level, encourage
curiosity, and use examples when useful.

Do not just give answers. Help the learner understand the reasoning.
"""


def ask_cynthia(message: str) -> str:
    result = chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": message,
            },
        ],
    )

    return result["message"]["content"]
