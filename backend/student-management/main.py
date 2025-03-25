from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import database
from pydantic import BaseModel

app = FastAPI()

# Pydantic model for request/response validation
class StudentCreate(BaseModel):
    name: str
    age: int
    email: str

class StudentResponse(StudentCreate):
    id: int

    class Config:
        orm_mode = True

# Initialize database on startup
@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=database.engine)

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/students/", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    db_student = db.query(models.Student).filter(models.Student.email == student.email).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new student
    db_student = models.Student(
        name=student.name,
        age=student.age,
        email=student.email
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students/{student_id}", response_model=StudentResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@app.get("/students/", response_model=List[StudentResponse])
def read_all_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    return students