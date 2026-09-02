from ollama import chat

MODEL = "qwen3:8b"

SYSTEM_PROMPT = """
You are Cynthia, the AI learning companion for Cynlith.

Your purpose is to help learners understand concepts deeply.
Explain clearly and simply, adapt to the learner's level, encourage
curiosity, and use examples when useful.

Do not just give answers. Help the learner understand the reasoning.
Maintain a natural, friendly conversation and use previous messages
when they are relevant.
"""


def ask_cynthia(message: str, history: list[dict] | None = None) -> str:
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    if history:
        messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": message,
        }
    )

    result = chat(
        model=MODEL,
        messages=messages,
    )

    return result["message"]["content"]
