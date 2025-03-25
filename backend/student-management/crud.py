from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session  # Add sync session support
from sqlalchemy.future import select
from sqlalchemy import or_
import models
import schemas
from passlib.context import CryptContext
from typing import Union  # For type hints

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
    # Check if email exists
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
    # Check if username exists
    if isinstance(db, AsyncSession):
        existing = await db.execute(select(models.User).filter(models.User.username == user.username))
    else:
        existing = db.execute(select(models.User).filter(models.User.username == user.username))
        
    if existing.scalars().first():
        raise DuplicateUsernameError("Username already registered")

    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
        is_active=True
    )
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
        or_(
            models.Student.name.ilike(f"%{search_term}%"),
            models.Student.email.ilike(f"%{search_term}%")
        )
    ).offset(skip).limit(limit)
    
    if isinstance(db, AsyncSession):
        result = await db.execute(query)
    else:
        result = db.execute(query)
        
    return result.scalars().all()