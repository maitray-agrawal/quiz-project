from fastapi import APIRouter, HTTPException
from app.database import students_col
from app.models import Student
from datetime import datetime

router = APIRouter(prefix="/students", tags=["students"])

# CREATE student
@router.post("/")
async def create_student(student: Student):
    try:
        student_dict = student.dict()
        student_dict["created_at"] = datetime.utcnow()

        result = students_col.insert_one(student_dict)

        return {
            "message": "Student added successfully",
            "id": str(result.inserted_id)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# GET all students
@router.get("/")
async def get_students():
    students = list(students_col.find({}, {"_id": 0}))
    return students