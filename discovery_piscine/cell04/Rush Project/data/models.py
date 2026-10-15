"""
models.py
---------
โครงสร้างฐานข้อมูล (ORM Models) สำหรับระบบจัดการข้อมูลหลักสูตรปริญญาตรี

ตาราง:
- Course                     : คลังรายวิชากลาง (รหัสวิชาเป็น Primary Key)
- CourseGroup                : หมวดวิชา / หมวดวิชาย่อย (รองรับลำดับชั้น parent-child)
- Curriculum                 : หลักสูตร
- CurriculumCourse           : ความสัมพันธ์ วิชา <-> หมวดย่อย <-> หลักสูตร
                                (บังคับ/เลือก, ปี/เทอมที่แนะนำ)
- CurriculumGroupRequirement : เงื่อนไขหน่วยกิตขั้นต่ำ/สูงสุด ต่อหมวดวิชา ต่อหลักสูตร
- CourseEquivalency          : คู่วิชาที่เทียบเคียงกันได้ข้ามหลักสูตร (สำหรับ 2 ปริญญา)
"""

from __future__ import annotations

import enum
from typing import Optional, List

from sqlalchemy import (
    ForeignKey,
    String,
    Text,
    Integer,
    Boolean,
    Enum as SAEnum,
    UniqueConstraint,
    CheckConstraint,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class GroupType(str, enum.Enum):
    GENED = "GENED"                             # ศึกษาทั่วไป (หมวดกลางของสถาบัน)
    MAJOR_REQUIRED = "MAJOR_REQUIRED"            # วิชาเฉพาะ - บังคับ
    MAJOR_ELECTIVE = "MAJOR_ELECTIVE"            # วิชาเฉพาะ - เลือกสาขา
    RESTRICTED_ELECTIVE = "RESTRICTED_ELECTIVE"  # วิชาเฉพาะ - บังคับเลือก
    FREE_ELECTIVE = "FREE_ELECTIVE"              # เลือกเสรี (เลือกวิชาใดก็ได้)


class EquivalenceType(str, enum.Enum):
    FULL = "FULL"        # เทียบเท่าเต็มหน่วยกิต
    PARTIAL = "PARTIAL"  # เทียบได้บางส่วน (ดู credit_equivalent)


class SemesterType(int, enum.Enum):
    FIRST = 1     # เทอม 1
    SECOND = 2    # เทอม 2
    SUMMER = 3    # ภาคฤดูร้อน


# ---------------------------------------------------------------------------
# Course : คลังรายวิชากลาง
# ---------------------------------------------------------------------------

class Course(Base):
    __tablename__ = "courses"

    code: Mapped[str] = mapped_column(String(20), primary_key=True)  # เช่น "CS101"
    name_th: Mapped[str] = mapped_column(String(255), nullable=False)
    name_en: Mapped[Optional[str]] = mapped_column(String(255))
    credits: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

    curriculum_links: Mapped[List["CurriculumCourse"]] = relationship(
        back_populates="course", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Course {self.code} - {self.name_th}>"


# ---------------------------------------------------------------------------
# CourseGroup : หมวดวิชา / หมวดวิชาย่อย (รองรับ hierarchy)
# ---------------------------------------------------------------------------

class CourseGroup(Base):
    __tablename__ = "course_groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    group_type: Mapped[GroupType] = mapped_column(SAEnum(GroupType), nullable=False)

    # หมวดย่อยอ้างอิงหมวดใหญ่ (self-referencing) — NULL = เป็นหมวดใหญ่ระดับบนสุด
    parent_group_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("course_groups.id", ondelete="CASCADE")
    )

    # NULL = หมวดกลางของสถาบัน (เช่น GenEd ใช้ร่วมกันทุกหลักสูตร)
    # มีค่า = หมวดเฉพาะของหลักสูตรนั้น (เช่น เลือกสาขา, บังคับเลือก)
    curriculum_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("curricula.id", ondelete="CASCADE")
    )

    parent: Mapped[Optional["CourseGroup"]] = relationship(
        remote_side="CourseGroup.id", back_populates="children"
    )
    children: Mapped[List["CourseGroup"]] = relationship(
        back_populates="parent", cascade="all, delete-orphan"
    )
    curriculum: Mapped[Optional["Curriculum"]] = relationship(
        back_populates="groups"
    )
    curriculum_courses: Mapped[List["CurriculumCourse"]] = relationship(
        back_populates="group"
    )
    requirements: Mapped[List["CurriculumGroupRequirement"]] = relationship(
        back_populates="group", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<CourseGroup {self.id} - {self.name} ({self.group_type.value})>"


# ---------------------------------------------------------------------------
# Curriculum : หลักสูตร
# ---------------------------------------------------------------------------

class Curriculum(Base):
    __tablename__ = "curricula"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    faculty: Mapped[Optional[str]] = mapped_column(String(255))
    year: Mapped[int] = mapped_column(Integer, nullable=False)  # ปีหลักสูตร (พ.ศ.)
    total_credits: Mapped[int] = mapped_column(Integer, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)  # ลำดับการแสดงผลใน dropdown/รายการ (น้อย=แสดงก่อน)

    groups: Mapped[List["CourseGroup"]] = relationship(
        back_populates="curriculum", cascade="all, delete-orphan"
    )
    courses: Mapped[List["CurriculumCourse"]] = relationship(
        back_populates="curriculum", cascade="all, delete-orphan"
    )
    requirements: Mapped[List["CurriculumGroupRequirement"]] = relationship(
        back_populates="curriculum", cascade="all, delete-orphan"
    )
    study_plans: Mapped[List["StudyPlan"]] = relationship(
        back_populates="curriculum", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Curriculum {self.id} - {self.name}>"


# ---------------------------------------------------------------------------
# StudyPlan : แผนทางเลือกภายในหลักสูตรเดียวกัน (เช่น แผนทำโครงงาน vs แผนสหกิจศึกษา)
# ---------------------------------------------------------------------------

class StudyPlan(Base):
    __tablename__ = "study_plans"
    __table_args__ = (
        UniqueConstraint("curriculum_id", "code", name="uq_study_plan_code"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    curriculum_id: Mapped[int] = mapped_column(
        ForeignKey("curricula.id", ondelete="CASCADE"), nullable=False
    )
    code: Mapped[str] = mapped_column(String(50), nullable=False)   # เช่น "PROJECT", "COOP"
    name: Mapped[str] = mapped_column(String(255), nullable=False)  # เช่น "แผนทำโครงงานพิเศษ"

    curriculum: Mapped["Curriculum"] = relationship(back_populates="study_plans")
    curriculum_courses: Mapped[List["CurriculumCourse"]] = relationship(
        back_populates="study_plan"
    )

    def __repr__(self) -> str:
        return f"<StudyPlan {self.code} - {self.name}>"


# ---------------------------------------------------------------------------
# CurriculumCourse : วิชา <-> หมวดย่อย <-> หลักสูตร (บังคับ/เลือก, ปี/เทอมที่แนะนำ)
# ---------------------------------------------------------------------------

class CurriculumCourse(Base):
    __tablename__ = "curriculum_courses"
    __table_args__ = (
        UniqueConstraint(
            "curriculum_id", "course_code", "group_id", "study_plan_id",
            name="uq_curriculum_course_group_plan",
        ),
        CheckConstraint(
            "recommended_semester IN (1, 2, 3)",
            name="ck_recommended_semester_valid",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    curriculum_id: Mapped[int] = mapped_column(
        ForeignKey("curricula.id", ondelete="CASCADE"), nullable=False
    )
    course_code: Mapped[str] = mapped_column(
        ForeignKey("courses.code", ondelete="CASCADE"), nullable=False
    )
    group_id: Mapped[int] = mapped_column(
        ForeignKey("course_groups.id", ondelete="CASCADE"), nullable=False
    )
    # NULL = วิชานี้ใช้เหมือนกันทุกแผนทางเลือกของหลักสูตร
    # มีค่า = วิชานี้อยู่เฉพาะแผนทางเลือกนั้น (เช่น เฉพาะแผนโครงงาน หรือเฉพาะแผนสหกิจศึกษา)
    study_plan_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("study_plans.id", ondelete="CASCADE")
    )

    # True = วิชาบังคับในหมวดนี้ (ต้องเรียนทุกตัว)
    # False = วิชาเลือกในหมวดนี้ (เลือกเรียนบางส่วนให้ครบ min_credits ของหมวด)
    is_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    recommended_year: Mapped[Optional[int]] = mapped_column(Integer)       # ปีที่แนะนำ 1-4
    recommended_semester: Mapped[Optional[int]] = mapped_column(Integer)   # เทอม 1/2/3(ฤดูร้อน)

    curriculum: Mapped["Curriculum"] = relationship(back_populates="courses")
    course: Mapped["Course"] = relationship(back_populates="curriculum_links")
    group: Mapped["CourseGroup"] = relationship(back_populates="curriculum_courses")
    study_plan: Mapped[Optional["StudyPlan"]] = relationship(back_populates="curriculum_courses")

    def __repr__(self) -> str:
        req = "บังคับ" if self.is_required else "เลือก"
        return f"<CurriculumCourse {self.course_code} [{req}] Y{self.recommended_year}/S{self.recommended_semester}>"


# ---------------------------------------------------------------------------
# CurriculumGroupRequirement : เงื่อนไขหน่วยกิตต่อหมวดวิชา ต่อหลักสูตร
# ---------------------------------------------------------------------------

class CurriculumGroupRequirement(Base):
    __tablename__ = "curriculum_group_requirements"
    __table_args__ = (
        UniqueConstraint(
            "curriculum_id", "group_id", name="uq_curriculum_group_requirement"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    curriculum_id: Mapped[int] = mapped_column(
        ForeignKey("curricula.id", ondelete="CASCADE"), nullable=False
    )
    group_id: Mapped[int] = mapped_column(
        ForeignKey("course_groups.id", ondelete="CASCADE"), nullable=False
    )
    min_credits: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    max_credits: Mapped[Optional[int]] = mapped_column(Integer)

    curriculum: Mapped["Curriculum"] = relationship(back_populates="requirements")
    group: Mapped["CourseGroup"] = relationship(back_populates="requirements")

    def __repr__(self) -> str:
        return f"<CurriculumGroupRequirement curriculum={self.curriculum_id} group={self.group_id} min={self.min_credits}>"


# ---------------------------------------------------------------------------
# ElectiveTermSlot : จำนวน "ช่องวิชาเลือก" ที่ต้องเลือกต่อหมวด ต่อเทอม ต่อแผนทางเลือก
# ใช้แสดงในหน้าแผนการศึกษารายเทอม เป็น placeholder (ไม่ผูกกับวิชาใดวิชาหนึ่งโดยเฉพาะ)
# แยกออกจาก CurriculumCourse เพราะเป็นข้อมูล "ต้องเลือกกี่วิชา" ไม่ใช่ "วิชาไหน"
# ---------------------------------------------------------------------------

class ElectiveTermSlot(Base):
    __tablename__ = "elective_term_slots"
    __table_args__ = (
        UniqueConstraint(
            "curriculum_id", "group_id", "study_plan_id", "year", "semester",
            name="uq_elective_term_slot",
        ),
        CheckConstraint("semester IN (1, 2, 3)", name="ck_elective_slot_semester_valid"),
        CheckConstraint("slot_count > 0", name="ck_elective_slot_count_positive"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    curriculum_id: Mapped[int] = mapped_column(
        ForeignKey("curricula.id", ondelete="CASCADE"), nullable=False
    )
    group_id: Mapped[int] = mapped_column(
        ForeignKey("course_groups.id", ondelete="CASCADE"), nullable=False
    )
    # NULL = ช่องนี้ใช้ร่วมกันทุกแผน (เช่น ปี 3 ที่ยังไม่แยกแผน)
    # มีค่า = ช่องนี้เฉพาะแผนทางเลือกนั้น (เช่น เฉพาะปี 4 แผนโครงงาน)
    study_plan_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("study_plans.id", ondelete="CASCADE")
    )
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    semester: Mapped[int] = mapped_column(Integer, nullable=False)
    slot_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)  # ต้องเลือกกี่วิชาในเทอมนี้จากหมวดนี้

    curriculum: Mapped["Curriculum"] = relationship()
    group: Mapped["CourseGroup"] = relationship()
    study_plan: Mapped[Optional["StudyPlan"]] = relationship()

    def __repr__(self) -> str:
        return f"<ElectiveTermSlot group={self.group_id} Y{self.year}/S{self.semester} x{self.slot_count}>"


# ---------------------------------------------------------------------------
# CourseGrade : ผลการเรียนรายวิชา (เกรดที่ได้) ต่อหลักสูตร — ใช้คำนวณความคืบหน้าการจบการศึกษา
# เก็บแบบผู้ใช้คนเดียว (ไม่มี Student entity) — ขอบเขตยังไม่รองรับหลายนักศึกษา
# ---------------------------------------------------------------------------

class CourseGrade(Base):
    __tablename__ = "course_grades"
    __table_args__ = (
        UniqueConstraint("curriculum_id", "course_code", name="uq_course_grade_curriculum_course"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    curriculum_id: Mapped[int] = mapped_column(
        ForeignKey("curricula.id", ondelete="CASCADE"), nullable=False
    )
    course_code: Mapped[str] = mapped_column(
        ForeignKey("courses.code", ondelete="CASCADE"), nullable=False
    )
    grade: Mapped[str] = mapped_column(String(2), nullable=False)  # A, B+, B, C+, C, D+, D, F, S, U
    # ปี/เทอมที่เรียนจริง (อาจต่างจาก recommended_year/semester ของหลักสูตรได้ เพราะเป็นของจริงที่นักศึกษาลงเอง)
    actual_year: Mapped[Optional[int]] = mapped_column(Integer)
    actual_semester: Mapped[Optional[int]] = mapped_column(Integer)

    curriculum: Mapped["Curriculum"] = relationship()
    course: Mapped["Course"] = relationship()

    def __repr__(self) -> str:
        return f"<CourseGrade {self.course_code} = {self.grade}>"


# ---------------------------------------------------------------------------
# CourseEquivalency : คู่วิชาที่เทียบเคียงกันได้ข้ามหลักสูตร (สำหรับ 2 ปริญญา)
# ---------------------------------------------------------------------------

class CourseEquivalency(Base):
    __tablename__ = "course_equivalencies"
    __table_args__ = (
        CheckConstraint(
            "course_code_a != course_code_b", name="ck_equivalency_not_self"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    course_code_a: Mapped[str] = mapped_column(
        ForeignKey("courses.code", ondelete="CASCADE"), nullable=False
    )
    course_code_b: Mapped[str] = mapped_column(
        ForeignKey("courses.code", ondelete="CASCADE"), nullable=False
    )
    equivalence_type: Mapped[EquivalenceType] = mapped_column(
        SAEnum(EquivalenceType), nullable=False, default=EquivalenceType.FULL
    )
    # ใช้เมื่อ equivalence_type = PARTIAL เช่น เทียบได้ 2 จาก 3 หน่วยกิต
    credit_equivalent: Mapped[Optional[int]] = mapped_column(Integer)
    note: Mapped[Optional[str]] = mapped_column(Text)

    course_a: Mapped["Course"] = relationship(foreign_keys=[course_code_a])
    course_b: Mapped["Course"] = relationship(foreign_keys=[course_code_b])

    def __repr__(self) -> str:
        return f"<CourseEquivalency {self.course_code_a} <-> {self.course_code_b} ({self.equivalence_type.value})>"
