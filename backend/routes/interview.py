from fastapi import APIRouter
from services.llm_service import generate_question, generate_next_question, generate_followup, generate_report
import uuid
from services.interview_service import (
    create_session,
    set_initial_question,
    add_interaction,
    should_ask_followup,
    advance_to_next_question,
    get_session,
    get_session_data
)
from fastapi import HTTPException

router = APIRouter()

@router.post("/start-interview")
def start_interview(data: dict):

    # error handling for missing keys
    if "role" not in data or "resume_text" not in data:
        raise HTTPException(status_code=400, detail="Missing required fields: 'role' and 'resume_text'.")

    role = data["role"]
    resume_text = data["resume_text"]
    company = data.get("company", "")

    session_id = str(uuid.uuid4())
    create_session(session_id, role, resume_text, company)

    question = generate_question(
        role,
        resume_text,
        company
    )

    set_initial_question(session_id, question)

    return {
        "session_id": session_id,
        "question": question
    }

@router.post("/answer")
def submit_answer(data: dict):

    # error handling for missing keys
    if "session_id" not in data or "question" not in data or "answer" not in data:
        raise HTTPException(status_code=400, detail="Missing required fields: 'session_id', 'question', and 'answer'.")

    session_id = data["session_id"]
    question = data["question"]
    answer = data["answer"]
    company = data.get("company", "")

    add_interaction(
        session_id,
        question,
        answer
    )

    session_data = get_session_data(session_id)
    history = get_session(session_id)
    role = session_data.get("role", "")
    resume_text = session_data.get("resume_text", "")
    target_company = session_data.get("company") or company

    if should_ask_followup(session_id):
        next_question = generate_followup(
            question,
            answer,
            target_company
        )
        is_followup = True
    else:
        next_question = generate_next_question(
            role,
            resume_text,
            target_company,
            history
        )
        advance_to_next_question(session_id, next_question)
        is_followup = False

    return {
        "question": next_question,
        "followup": next_question,
        "is_followup": is_followup
    }

@router.post("/end-interview")
def end_interview(data: dict):

    # error handling for missing keys
    if "session_id" not in data:
        raise HTTPException(status_code=400, detail="Missing required field: 'session_id'.")

    session_id = data["session_id"]

    session_data = get_session_data(session_id)
    history = get_session(session_id)
    role = session_data.get("role", "")
    company = session_data.get("company", "")

    report = generate_report(history, role, company)

    return {
        "report": report
    }