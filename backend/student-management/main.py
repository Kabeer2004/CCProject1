# main.py
import logging
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

# Local imports
from database import async_engine as engine, Base, get_db
import models
import crud
import schemas
from logging_config import setup_logging
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

logger = logging.getLogger(__name__)
setup_logging()

app = FastAPI(title="Student Management API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await crud.get_user_by_username(db, username)
    if not user or not pwd_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        return response
    except Exception as e:
        logger.exception(f"Exception: {str(e)}")
        raise

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/students/", response_model=schemas.Student, status_code=status.HTTP_201_CREATED)
async def create_student(student: schemas.StudentCreate, db: AsyncSession = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    try:
        return await crud.create_student(db=db, student=student)
    except crud.DuplicateEmailError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/students/", response_model=list[schemas.Student])
async def read_students(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return await crud.get_students(db, skip=skip, limit=limit)

@app.get("/students/{student_id}", response_model=schemas.Student)
async def read_student(student_id: int, db: AsyncSession = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_student = await crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return db_student

@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    return await crud.create_user(db=db, user=user)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# New endpoints
@app.post("/courses/", response_model=schemas.Course, status_code=status.HTTP_201_CREATED)
async def create_course(course: schemas.CourseCreate, db: AsyncSession = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return await crud.create_course(db=db, course=course)

@app.get("/courses/{course_id}", response_model=schemas.Course)
async def read_course(course_id: int, db: AsyncSession = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_course = await crud.get_course(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course

@app.post("/enrollments", response_model=dict)
async def enroll_student(enrollment: schemas.EnrollmentCreate, db: AsyncSession = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    await crud.create_enrollment(db=db, enrollment=enrollment)
    return {"message": "Enrollment successful"}

@app.get("/students/{student_id}/courses/", response_model=schemas.StudentEnrolledCourses)
async def read_student_courses(student_id: int, db: AsyncSession = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    courses = await crud.get_enrolled_courses(db, student_id=student_id)
    return {"enrolled_courses": courses}