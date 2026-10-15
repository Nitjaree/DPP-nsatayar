"""
database.py
------------
ตั้งค่าการเชื่อมต่อฐานข้อมูล SQLite และให้ฟังก์ชันสำหรับสร้างตาราง / เปิด session
"""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .models import Base

DB_DIR = Path(__file__).resolve().parent
DB_PATH = DB_DIR / "database.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# check_same_thread=False จำเป็นสำหรับแอป Desktop ที่อาจเรียกใช้ session จากหลาย thread (เช่น Qt UI thread)
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    """สร้างตารางทั้งหมดตาม models.py (ถ้ายังไม่มี)"""
    Base.metadata.create_all(bind=engine)


def get_session() -> Session:
    """เปิด session ใหม่สำหรับใช้งานกับฐานข้อมูล"""
    return SessionLocal()


if __name__ == "__main__":
    init_db()
    print(f"สร้างฐานข้อมูลเรียบร้อยที่: {DB_PATH}")
