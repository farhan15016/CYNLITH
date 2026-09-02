from backend.study import StudySession
from fastapi import FastAPI
from pydantic import BaseModel

from ai.cynthia import ask_cynthia
from backend.database import (
    init_db,
    save_message,
    get_messages,
    get_memories,
    save_profile,
    get_profile,
    save_subject,
    get_subjects,
)

app = FastAPI(title="Cynlith API")

init_db()


class ChatRequest(BaseModel):
    message: str
    subject: str | None = None


class ChatResponse(BaseModel):
    response: str


class ProfileRequest(BaseModel):
    key: str
    value: str


class SubjectRequest(BaseModel):
    subject: str
    level: str

class StudySessionRequest(BaseModel):
    subject: str
    topic: str
    level: str
    mode: str = "STANDARD"


@app.get("/")
def root():
    return {
        "status": "ok",
        "assistant": "Cynthia"
    }


@app.post("/study-session")
def create_study_session(request: StudySessionRequest):
    session = StudySession(
        subject=request.subject,
        topic=request.topic,
        level=request.level,
        mode=request.mode,
    )

    lesson = session.generate_lesson()

    return {
        "status": "created",
        "session": session.__dict__,
        "lesson": lesson,
    }

@app.get("/profile")
def profile():
    return {
        "profile": get_profile()
    }


@app.post("/profile")
def update_profile(request: ProfileRequest):
    save_profile(request.key, request.value)

    return {
        "status": "saved",
        "profile": get_profile()
    }


@app.get("/subjects")
def subjects():
    return {
        "subjects": get_subjects()
    }


@app.post("/subjects")
def update_subject(request: SubjectRequest):
    save_subject(request.subject, request.level)

    return {
        "status": "saved",
        "subjects": get_subjects()
    }


@app.post("/chat", response_model=ChatResponse)
def chat_with_cynthia(request: ChatRequest):
    history = get_messages()[-20:]
    profile_data = get_profile()
    subjects_data = get_subjects()
    memories = get_memories()

    context_parts = []

    if request.subject:
        current_level = next(
            (
                item["level"]
                for item in subjects_data
                if item["subject"].lower() == request.subject.lower()
            ),
            None,
        )

        context_parts.append(
            f"Current learning subject: {request.subject}"
        )

        if current_level:
            context_parts.append(
                f"Current subject proficiency: {current_level}"
            )

    if profile_data:
        profile_context = "\n".join(
            f"{item['key']}: {item['value']}"
            for item in profile_data
        )

        context_parts.append(
            f"Learner profile:\n{profile_context}"
        )

    if subjects_data:
        subject_context = "\n".join(
            f"{item['subject']}: {item['level']}"
            for item in subjects_data
        )

        context_parts.append(
            f"Learner subjects and levels:\n{subject_context}"
        )

    if memories:
        memory_context = "\n".join(
            f"{item['key']}: {item['value']}"
            for item in memories
        )

        context_parts.append(
            f"Known learner information:\n{memory_context}"
        )

    learner_context = "\n\n".join(context_parts)

    response = ask_cynthia(
        message=request.message,
        history=history,
        learner_context=learner_context,
    )

    save_message("user", request.message)
    save_message("assistant", response)

    return ChatResponse(response=response)
