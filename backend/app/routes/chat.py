from fastapi import APIRouter
from app.models import ChatRequest
from app.database import students_col
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os, json

load_dotenv()
router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/")
async def chat_with_data(req: ChatRequest):
    # LLM created here — after load_dotenv() has run
    llm = ChatGroq(
    model="llama3-8b-8192",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are EduLens, an AI assistant for educators.
         Answer questions about student performance using the provided data.
         Be concise, specific, and actionable.
         Student data: {context}"""),
        ("human", "{question}")
    ])

    students = list(students_col.find({}, {"_id": 0, "name": 1,
        "student_id": 1, "attendance_pct": 1,
        "risk_tier": 1, "assessments": 1}).limit(50))

    context = json.dumps(students, default=str, indent=2)
    chain = prompt | llm
    response = chain.invoke({"context": context, "question": req.question})
    return {"answer": response.content}