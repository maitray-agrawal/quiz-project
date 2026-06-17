from fastapi import APIRouter, HTTPException
from app.models import PredictRequest
from app.ml.explain import get_explanation
from app.database import students_col

router = APIRouter(prefix="/predict", tags=["predict"])

@router.post("/student")
async def predict_student(req: PredictRequest):
    student = students_col.find_one({"student_id": req.student_id}, {"_id": 0})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Build feature dict from student record
    assessments = student.get("assessments", [])
    avg_score = sum(a["score"] for a in assessments) / len(assessments) if assessments else 0
    
    features = {
        "attendance_pct": student.get("attendance_pct", 0),
        "avg_score": avg_score,
        "assignments_submitted": len(assessments),
        "quiz_avg": avg_score * 0.9,       # simplified
        "study_hours_week": 10.0,           # default; extend schema later
    }
    
    result = get_explanation(features)
    
    # Persist risk tier back to student record
    students_col.update_one(
        {"student_id": req.student_id},
        {"$set": {"risk_tier": result["risk_tier"]}}
    )
    
    return result