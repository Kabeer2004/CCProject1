from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
import os

# Database URLs
ASYNC_SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./students.db"
SYNC_SQLALCHEMY_DATABASE_URL = "sqlite:///./students.db"
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Engines
async_engine = create_async_engine(
    ASYNC_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

sync_engine = create_engine(
    SYNC_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

test_engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

# Session makers
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False
)

TestSessionLocal = sessionmaker(
    bind=test_engine,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

def get_sync_db():
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_test_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()