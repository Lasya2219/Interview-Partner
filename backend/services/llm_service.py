import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"   
)

def generate_question(role, resume_text, company):

    prompt = f"""
    You are an experienced technical interviewer.

    Candidate Role:
    {role}

    Target Company:
    {company}

    Resume:
    {resume_text}

    Instructions:
    - Ask ONLY ONE interview question.
    - The question should be concise (2-3 sentences maximum).
    - Base it on the candidate's resume, selected role, and target company.
    - Mix technical, behavioral, and company-specific questions across the interview, but ask only ONE question at a time.
    - Do NOT generate a list of questions.
    - Do NOT explain your reasoning.
    - Do NOT use headings or bullet points.

    Return only the interview question.
    """
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        print(f"Error generating interview question: {e}")
        return "Sorry, I'm having trouble generating a question right now."

def generate_next_question(role, resume_text, company, history):

    formatted_history = "\n".join([f"Q: {item.get('question', '')}\nA: {item.get('answer', '')}" for item in history])

    prompt = f"""
    You are an experienced technical interviewer conducting a live, multi-topic interview.

    Candidate Role:
    {role}

    Target Company:
    {company}

    Resume:
    {resume_text}

    Questions & Answers asked so far:
    {formatted_history}

    Instructions:
    - Ask ONLY ONE brand new interview question.
    - Transition to a COMPLETELY DIFFERENT topic or area from the previous questions (e.g., if previous questions focused on a specific project, switch to core technical fundamentals, system architecture, debugging, or behavioral/collaboration).
    - Do NOT ask a follow-up to the previous question.
    - Do NOT repeat or overlap with any topic or question already covered.
    - The question should be concise (1-2 sentences maximum).
    - Do NOT explain your reasoning.
    - Do NOT use headings or bullet points.

    Return only the interview question.
    """
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        print(f"Error generating next interview question: {e}")
        return "Sorry, I'm having trouble generating a question right now."

def generate_followup(question, answer, company):

    prompt = f"""
    You are an experienced interviewer conducting a conversational interview.

    Target Company:
    {company}

    Previous Question:
    {question}

    Candidate Answer:
    {answer}

    Instructions:
    - Ask ONLY ONE follow-up question directly related to what the candidate just answered.
    - Keep it under 2 sentences.
    - Probe for a practical detail, edge case, or specific trade-off from their answer.
    - Do NOT ask them to recite textbook essays or lengthy definitions.
    - If appropriate, relate it to expectations for {company}.
    - Do not provide feedback.
    - Do not answer the previous question.
    - Do not generate multiple questions.

    Return only the follow-up question.
    """
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        print(f"Error generating follow-up question: {e}")
        return "Sorry, I'm having trouble generating a follow-up question right now."   


def evaluate_answer(question, answer):

    prompt = f"""
    You are an experienced technical interviewer evaluating a spoken interview response.

    Interview Question:
    {question}

    Candidate Answer:
    {answer}

    Instructions:
    - In a real verbal interview, concise and direct answers (2-3 sentences) are strong communication.
    - Do NOT penalize brevity if the core concept or logic is correct.
    - Do NOT complain that the answer 'should have been in more detail'.
    - Evaluate based on technical correctness, clarity, and practical understanding.

    Provide:

    1. Technical Score (/10)
    2. Brief Feedback (2-3 sentences)
    3. One practical suggestion for improvement

    Keep the evaluation realistic and professional.
    """

    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        print(f"Error evaluating answers: {e}")
        return "Sorry, I'm having trouble evaluating your answers right now."  


def generate_report(history, role="", company=""):

    prompt = f"""
    You are a realistic, professional interview evaluator assessing a spoken/conversational interview.

    Role:
    {role}

    Target Company:
    {company}

    Interview History:
    {history}

    Important Evaluation Guidelines:
    - This was a live spoken interview. Candidates give concise, practical verbal answers (typically 2-4 sentences).
    - Do NOT penalize candidates simply for being concise. A focused, direct answer that addresses the core question is good communication, not a weakness.
    - Do NOT give generic complaints such as 'should have been in more detail', 'needs more depth', or 'should have provided more thorough explanations'.
    - Instead, evaluate whether the core concepts, technical logic, and trade-offs are sound and accurate.
    - In Strengths and Weaknesses, be concrete and specific about what technical ideas or approaches were good or missing, rather than commenting on word count or length.

    Provide:

    1. Overall Score (/10)
    2. Technical Knowledge Score (/10)
    3. Communication Score (/10)
    4. Strengths (concrete points the candidate explained well)
    5. Weaknesses (specific technical gaps, misconceptions, or omitted trade-offs, if any)
    6. Areas for Improvement (actionable advice)
    7. Recommended Topics to Study

    Keep the report professional, realistic, and constructive.
    """
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        print(f"Error generating Report: {e}")
        return "Sorry, I'm having trouble generating Report."  
