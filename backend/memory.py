import json
from pathlib import Path

MEMORY_FILE = Path(__file__).parent / "conversation_memory.json"


def load_memory() -> list[dict]:
    if not MEMORY_FILE.exists():
        return []

    with open(MEMORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_memory(history: list[dict]) -> None:
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=2)


def add_memory(role: str, content: str) -> None:
    history = load_memory()
    history.append({
        "role": role,
        "content": content
    })
    save_memory(history)


def get_history() -> list[dict]:
    return load_memory()
