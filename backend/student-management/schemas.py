# schemas.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional

class StudentBase(BaseModel):
    name: str
    age: int
    email: EmailStr

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

# New schemas for courses and enrollments
class CourseBase(BaseModel):
    title: str
    description: str

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int

    class Config:
        orm_mode = True

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int

class StudentEnrolledCourses(BaseModel):
    enrolled_courses: List[int]