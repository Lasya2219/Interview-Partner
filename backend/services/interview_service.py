import random

interview_sessions = {}

def create_session(session_id, role="", resume_text="", company=""):
    interview_sessions[session_id] = {
        "role": role,
        "resume_text": resume_text,
        "company": company,
        "history": [],
        "current_main_question": "",
        "followup_count": 0,
        "max_followups": random.randint(1, 2)
    }

def set_initial_question(session_id, question):
    if session_id in interview_sessions:
        interview_sessions[session_id]["current_main_question"] = question
        interview_sessions[session_id]["followup_count"] = 0

def add_interaction(session_id, question, answer):
    if session_id not in interview_sessions:
        raise ValueError(f"Session ID {session_id} does not exist.")

    session = interview_sessions[session_id]
    session["history"].append({
        "question": question,
        "answer": answer
    })
    session["followup_count"] += 1

def should_ask_followup(session_id):
    if session_id not in interview_sessions:
        return False

    session = interview_sessions[session_id]
    return session["followup_count"] < session["max_followups"]

def advance_to_next_question(session_id, new_question):
    if session_id in interview_sessions:
        session = interview_sessions[session_id]
        session["current_main_question"] = new_question
        session["followup_count"] = 0
        session["max_followups"] = random.randint(1, 2)

def get_session(session_id):
    if session_id not in interview_sessions:
        return []

    session = interview_sessions.get(session_id, [])
    if isinstance(session, list):
        return session

    return session.get("history", [])

def get_session_data(session_id):
    return interview_sessions.get(session_id, {})