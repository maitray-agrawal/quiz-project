from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Assessment(BaseModel):
    subject: str
    score: float
    max_score: float
    date: datetime


class Student(BaseModel):
    student_id: str
    name: str
    age: int
    gender: str
    attendance_pct: float
    assessments: List[Assessment] = []
    risk_tier: Optional[str] = None
    created_at: Optional[datetime] = None


class PredictRequest(BaseModel):
    student_id: str


class ChatRequest(BaseModel):
    question: str