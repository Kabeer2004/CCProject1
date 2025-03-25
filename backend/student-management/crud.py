# crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import or_
from passlib.context import CryptContext
from typing import Union
from fastapi import HTTPException
import models
import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class DuplicateEmailError(Exception):
    pass

class DuplicateUsernameError(Exception):
    pass

async def get_student(db: Union[AsyncSession, Session], student_id: int):
    if isinstance(db, AsyncSession):
        result = await db.execute(select(models.Student).filter(models.Student.id == student_id))
    else:
        result = db.execute(select(models.Student).filter(models.Student.id == student_id))
    return result.scalars().first()

async def get_students(db: Union[AsyncSession, Session], skip: int = 0, limit: int = 100):
    if isinstance(db, AsyncSession):
        result = await db.execute(select(models.Student).offset(skip).limit(limit))
    else:
        result = db.execute(select(models.Student).offset(skip).limit(limit))
    return result.scalars().all()

async def create_student(db: Union[AsyncSession, Session], student: schemas.StudentCreate):
    if isinstance(db, AsyncSession):
        existing = await db.execute(select(models.Student).filter(models.Student.email == student.email))
    else:
        existing = db.execute(select(models.Student).filter(models.Student.email == student.email))
    if existing.scalars().first():
        raise DuplicateEmailError("Email already registered")
    db_student = models.Student(**student.dict())
    db.add(db_student)
    if isinstance(db, AsyncSession):
        await db.commit()
        await db.refresh(db_student)
    else:
        db.commit()
        db.refresh(db_student)
    return db_student

async def get_user_by_username(db: Union[AsyncSession, Session], username: str):
    if isinstance(db, AsyncSession):
        result = await db.execute(select(models.User).filter(models.User.username == username))
    else:
        result = db.execute(select(models.User).filter(models.User.username == username))
    return result.scalars().first()

async def create_user(db: Union[AsyncSession, Session], user: schemas.UserCreate):
    if isinstance(db, AsyncSession):
        existing = await db.execute(select(models.User).filter(models.User.username == user.username))
    else:
        existing = db.execute(select(models.User).filter(models.User.username == user.username))
    if existing.scalars().first():
        raise DuplicateUsernameError("Username already registered")
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password, is_active=True)
    db.add(db_user)
    if isinstance(db, AsyncSession):
        await db.commit()
        await db.refresh(db_user)
    else:
        db.commit()
        db.refresh(db_user)
    return db_user

async def search_students(db: Union[AsyncSession, Session], search_term: str, skip: int = 0, limit: int = 100):
    query = select(models.Student).where(
        or_(models.Student.name.ilike(f"%{search_term}%"), models.Student.email.ilike(f"%{search_term}%"))
    ).offset(skip).limit(limit)
    if isinstance(db, AsyncSession):
        result = await db.execute(query)
    else:
        result = db.execute(query)
    return result.scalars().all()

# New CRUD functions
async def create_course(db: AsyncSession, course: schemas.CourseCreate):
    db_course = models.Course(**course.dict())
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    return db_course

async def get_course(db: AsyncSession, course_id: int):
    result = await db.execute(select(models.Course).filter(models.Course.id == course_id))
    return result.scalars().first()

async def create_enrollment(db: AsyncSession, enrollment: schemas.EnrollmentCreate):
    student = await get_student(db, enrollment.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    course = await get_course(db, enrollment.course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    existing_enrollment = await db.execute(
        select(models.Enrollment).filter(
            models.Enrollment.student_id == enrollment.student_id,
            models.Enrollment.course_id == enrollment.course_id
        )
    )
    if existing_enrollment.scalars().first():
        raise HTTPException(status_code=400, detail="Already enrolled")
    db_enrollment = models.Enrollment(**enrollment.dict())
    db.add(db_enrollment)
    await db.commit()
    await db.refresh(db_enrollment)
    return db_enrollment

async def get_enrolled_courses(db: AsyncSession, student_id: int):
    student = await get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    result = await db.execute(
        select(models.Enrollment.course_id).filter(models.Enrollment.student_id == student_id)
    )
    return result.scalars().all()