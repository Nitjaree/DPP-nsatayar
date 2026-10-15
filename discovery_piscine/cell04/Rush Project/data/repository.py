"""
repository.py
--------------
ชั้นเข้าถึงข้อมูล (Data Access Layer) — ฟังก์ชัน CRUD และ query ที่ใช้บ่อย
สำหรับทุกตารางใน models.py

แนวทางการใช้งาน:
- ทุกฟังก์ชันรับ `session: Session` เป็นพารามิเตอร์แรกเสมอ (เปิดผ่าน database.get_session())
- ฟังก์ชันที่เขียนข้อมูล (create/update/delete) จะ commit ให้ภายในฟังก์ชันเลย
  เพื่อให้ชั้น UI (application layer) เรียกใช้ได้ตรงไปตรงมา ไม่ต้องจัดการ transaction เอง
- ฟังก์ชันที่อ่านข้อมูล (get/list) จะไม่ commit เพราะไม่มีการเปลี่ยนแปลงข้อมูล
- ฟังก์ชัน get_* คืนค่า None ถ้าไม่พบข้อมูล ไม่โยน exception

ตัวอย่างการใช้งาน:
    from data.database import get_session
    from data import repository as repo

    session = get_session()
    course = repo.create_course(session, code="01236611", name_th="พื้นฐานระบบไอโอที", credits=3)
    session.close()
"""

from __future__ import annotations

from typing import Optional, List, Dict

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import (
    Course,
    CourseGroup,
    Curriculum,
    StudyPlan,
    CurriculumCourse,
    CurriculumGroupRequirement,
    CourseEquivalency,
    ElectiveTermSlot,
    CourseGrade,
    GroupType,
    EquivalenceType,
)

# เกรดที่รองรับ เรียงจากดีที่สุดไปแย่ที่สุด (ใช้ประกอบ dropdown ในหน้า UI)
GRADE_CHOICES = ["A", "B+", "B", "C+", "C", "D+", "D", "F", "S", "U"]
# เกรดที่ถือว่า "ผ่าน" นับหน่วยกิตให้ (F และ U ถือว่าไม่ผ่าน)
PASSING_GRADES = {"A", "B+", "B", "C+", "C", "D+", "D", "S"}


# ===========================================================================
# Course
# ===========================================================================

def create_course(
    session: Session, code: str, name_th: str, credits: int,
    name_en: Optional[str] = None, description: Optional[str] = None,
) -> Course:
    course = Course(code=code, name_th=name_th, name_en=name_en, credits=credits, description=description)
    session.add(course)
    session.commit()
    session.refresh(course)
    return course


def get_course(session: Session, code: str) -> Optional[Course]:
    return session.get(Course, code)


def list_courses(session: Session, search: Optional[str] = None) -> List[Course]:
    """search: ถ้าระบุ จะกรองจากรหัสวิชาหรือชื่อวิชา (ไทย/อังกฤษ) แบบ partial match"""
    stmt = select(Course).order_by(Course.code)
    if search:
        like = f"%{search}%"
        stmt = stmt.where(
            (Course.code.like(like)) | (Course.name_th.like(like)) | (Course.name_en.like(like))
        )
    return list(session.scalars(stmt).all())


def update_course(session: Session, code: str, **fields) -> Optional[Course]:
    """fields ที่แก้ได้: name_th, name_en, credits, description"""
    course = session.get(Course, code)
    if course is None:
        return None
    for key, value in fields.items():
        if hasattr(course, key):
            setattr(course, key, value)
    session.commit()
    session.refresh(course)
    return course


def delete_course(session: Session, code: str) -> bool:
    course = session.get(Course, code)
    if course is None:
        return False
    session.delete(course)
    session.commit()
    return True


# ===========================================================================
# CourseGroup
# ===========================================================================

def create_course_group(
    session: Session, name: str, group_type: GroupType,
    parent_group_id: Optional[int] = None, curriculum_id: Optional[int] = None,
) -> CourseGroup:
    group = CourseGroup(
        name=name, group_type=group_type,
        parent_group_id=parent_group_id, curriculum_id=curriculum_id,
    )
    session.add(group)
    session.commit()
    session.refresh(group)
    return group


def get_course_group(session: Session, group_id: int) -> Optional[CourseGroup]:
    return session.get(CourseGroup, group_id)


def list_course_groups(
    session: Session, curriculum_id: Optional[int] = None, top_level_only: bool = False,
) -> List[CourseGroup]:
    """
    curriculum_id=None  -> คืนทุกกลุ่ม (รวม GenEd กลาง + ทุกหลักสูตร)
    curriculum_id=<id>  -> คืนเฉพาะกลุ่มของหลักสูตรนั้น + กลุ่ม GenEd กลาง (curriculum_id IS NULL)
    top_level_only=True -> คืนเฉพาะหมวดใหญ่ (parent_group_id IS NULL) ไม่รวมหมวดย่อย
    """
    stmt = select(CourseGroup)
    if curriculum_id is not None:
        stmt = stmt.where((CourseGroup.curriculum_id == curriculum_id) | (CourseGroup.curriculum_id.is_(None)))
    if top_level_only:
        stmt = stmt.where(CourseGroup.parent_group_id.is_(None))
    return list(session.scalars(stmt).all())


def get_group_children(session: Session, group_id: int) -> List[CourseGroup]:
    stmt = select(CourseGroup).where(CourseGroup.parent_group_id == group_id)
    return list(session.scalars(stmt).all())


def update_course_group(session: Session, group_id: int, **fields) -> Optional[CourseGroup]:
    """fields ที่แก้ได้: name, group_type, parent_group_id, curriculum_id"""
    group = session.get(CourseGroup, group_id)
    if group is None:
        return None
    for key, value in fields.items():
        if hasattr(group, key):
            setattr(group, key, value)
    session.commit()
    session.refresh(group)
    return group


def delete_course_group(session: Session, group_id: int) -> bool:
    group = session.get(CourseGroup, group_id)
    if group is None:
        return False
    session.delete(group)  # cascade ลบหมวดย่อย + CurriculumCourse + CurriculumGroupRequirement ที่ผูกอยู่ด้วย
    session.commit()
    return True


# ===========================================================================
# Curriculum
# ===========================================================================

def create_curriculum(
    session: Session, name: str, year: int, total_credits: int,
    faculty: Optional[str] = None, display_order: int = 0,
) -> Curriculum:
    curriculum = Curriculum(
        name=name, year=year, total_credits=total_credits, faculty=faculty, display_order=display_order,
    )
    session.add(curriculum)
    session.commit()
    session.refresh(curriculum)
    return curriculum


def get_curriculum(session: Session, curriculum_id: int) -> Optional[Curriculum]:
    return session.get(Curriculum, curriculum_id)


def list_curricula(session: Session) -> List[Curriculum]:
    return list(session.scalars(select(Curriculum).order_by(Curriculum.display_order, Curriculum.name)).all())


def update_curriculum(session: Session, curriculum_id: int, **fields) -> Optional[Curriculum]:
    """fields ที่แก้ได้: name, faculty, year, total_credits, display_order"""
    curriculum = session.get(Curriculum, curriculum_id)
    if curriculum is None:
        return None
    for key, value in fields.items():
        if hasattr(curriculum, key):
            setattr(curriculum, key, value)
    session.commit()
    session.refresh(curriculum)
    return curriculum


def delete_curriculum(session: Session, curriculum_id: int) -> bool:
    curriculum = session.get(Curriculum, curriculum_id)
    if curriculum is None:
        return False
    session.delete(curriculum)  # cascade ลบ groups/courses/requirements/study_plans เฉพาะของหลักสูตรนี้
    session.commit()
    return True


# ===========================================================================
# StudyPlan
# ===========================================================================

def create_study_plan(session: Session, curriculum_id: int, code: str, name: str) -> StudyPlan:
    plan = StudyPlan(curriculum_id=curriculum_id, code=code, name=name)
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan


def get_study_plan(session: Session, plan_id: int) -> Optional[StudyPlan]:
    return session.get(StudyPlan, plan_id)


def list_study_plans(session: Session, curriculum_id: int) -> List[StudyPlan]:
    stmt = select(StudyPlan).where(StudyPlan.curriculum_id == curriculum_id).order_by(StudyPlan.code)
    return list(session.scalars(stmt).all())


def update_study_plan(session: Session, plan_id: int, **fields) -> Optional[StudyPlan]:
    """fields ที่แก้ได้: code, name"""
    plan = session.get(StudyPlan, plan_id)
    if plan is None:
        return None
    for key, value in fields.items():
        if hasattr(plan, key):
            setattr(plan, key, value)
    session.commit()
    session.refresh(plan)
    return plan


def delete_study_plan(session: Session, plan_id: int) -> bool:
    plan = session.get(StudyPlan, plan_id)
    if plan is None:
        return False
    session.delete(plan)
    session.commit()
    return True


# ===========================================================================
# CurriculumCourse (วิชา <-> หมวดย่อย <-> หลักสูตร <-> แผนทางเลือก)
# ===========================================================================

def link_course_to_curriculum(
    session: Session, curriculum_id: int, course_code: str, group_id: int,
    is_required: bool = True, recommended_year: Optional[int] = None,
    recommended_semester: Optional[int] = None, study_plan_id: Optional[int] = None,
) -> CurriculumCourse:
    link = CurriculumCourse(
        curriculum_id=curriculum_id, course_code=course_code, group_id=group_id,
        is_required=is_required, recommended_year=recommended_year,
        recommended_semester=recommended_semester, study_plan_id=study_plan_id,
    )
    session.add(link)
    session.commit()
    session.refresh(link)
    return link


def get_curriculum_course(session: Session, link_id: int) -> Optional[CurriculumCourse]:
    return session.get(CurriculumCourse, link_id)


def list_courses_for_curriculum(
    session: Session, curriculum_id: int,
    group_id: Optional[int] = None,
    study_plan_id: Optional[int] = None,
    recommended_year: Optional[int] = None,
    include_shared_study_plan_courses: bool = True,
) -> List[CurriculumCourse]:
    """
    ดึงรายวิชาทั้งหมดของหลักสูตร พร้อมกรองได้ตามหมวด/แผนทางเลือก/ปีที่เรียน

    study_plan_id ระบุ -> คืนวิชาของแผนนั้น บวกวิชาที่ study_plan_id เป็น NULL (ใช้ร่วมกันทุกแผน)
                           เว้นแต่ include_shared_study_plan_courses=False จะคืนเฉพาะวิชาของแผนนั้นตรงๆ
    """
    stmt = select(CurriculumCourse).where(CurriculumCourse.curriculum_id == curriculum_id)
    if group_id is not None:
        stmt = stmt.where(CurriculumCourse.group_id == group_id)
    if recommended_year is not None:
        stmt = stmt.where(CurriculumCourse.recommended_year == recommended_year)
    if study_plan_id is not None:
        if include_shared_study_plan_courses:
            stmt = stmt.where(
                (CurriculumCourse.study_plan_id == study_plan_id) | (CurriculumCourse.study_plan_id.is_(None))
            )
        else:
            stmt = stmt.where(CurriculumCourse.study_plan_id == study_plan_id)
    return list(session.scalars(stmt).all())


def update_curriculum_course(session: Session, link_id: int, **fields) -> Optional[CurriculumCourse]:
    """fields ที่แก้ได้: group_id, is_required, recommended_year, recommended_semester, study_plan_id"""
    link = session.get(CurriculumCourse, link_id)
    if link is None:
        return None
    for key, value in fields.items():
        if hasattr(link, key):
            setattr(link, key, value)
    session.commit()
    session.refresh(link)
    return link


def unlink_course_from_curriculum(session: Session, link_id: int) -> bool:
    link = session.get(CurriculumCourse, link_id)
    if link is None:
        return False
    session.delete(link)
    session.commit()
    return True


# ===========================================================================
# CurriculumGroupRequirement (เงื่อนไขหน่วยกิตต่อหมวด ต่อหลักสูตร)
# ===========================================================================

def set_group_requirement(
    session: Session, curriculum_id: int, group_id: int,
    min_credits: int, max_credits: Optional[int] = None,
) -> CurriculumGroupRequirement:
    """สร้างใหม่ถ้ายังไม่มี หรืออัปเดตถ้ามีอยู่แล้ว (upsert ตาม curriculum_id + group_id)"""
    stmt = select(CurriculumGroupRequirement).where(
        CurriculumGroupRequirement.curriculum_id == curriculum_id,
        CurriculumGroupRequirement.group_id == group_id,
    )
    requirement = session.scalars(stmt).first()
    if requirement is None:
        requirement = CurriculumGroupRequirement(
            curriculum_id=curriculum_id, group_id=group_id,
            min_credits=min_credits, max_credits=max_credits,
        )
        session.add(requirement)
    else:
        requirement.min_credits = min_credits
        requirement.max_credits = max_credits
    session.commit()
    session.refresh(requirement)
    return requirement


def get_group_requirement(session: Session, requirement_id: int) -> Optional[CurriculumGroupRequirement]:
    return session.get(CurriculumGroupRequirement, requirement_id)


def list_group_requirements(session: Session, curriculum_id: int) -> List[CurriculumGroupRequirement]:
    stmt = select(CurriculumGroupRequirement).where(CurriculumGroupRequirement.curriculum_id == curriculum_id)
    return list(session.scalars(stmt).all())


def delete_group_requirement(session: Session, requirement_id: int) -> bool:
    requirement = session.get(CurriculumGroupRequirement, requirement_id)
    if requirement is None:
        return False
    session.delete(requirement)
    session.commit()
    return True


# ===========================================================================
# CourseEquivalency (คู่วิชาเทียบเคียงข้ามหลักสูตร)
# ===========================================================================

def create_course_equivalency(
    session: Session, course_code_a: str, course_code_b: str,
    equivalence_type: EquivalenceType = EquivalenceType.FULL,
    credit_equivalent: Optional[int] = None, note: Optional[str] = None,
) -> CourseEquivalency:
    equivalency = CourseEquivalency(
        course_code_a=course_code_a, course_code_b=course_code_b,
        equivalence_type=equivalence_type, credit_equivalent=credit_equivalent, note=note,
    )
    session.add(equivalency)
    session.commit()
    session.refresh(equivalency)
    return equivalency


def get_course_equivalency(session: Session, equivalency_id: int) -> Optional[CourseEquivalency]:
    return session.get(CourseEquivalency, equivalency_id)


def find_equivalent_courses(session: Session, course_code: str) -> List[Course]:
    """คืนรายวิชาทั้งหมดที่เทียบเคียงได้กับ course_code (มองทั้งสองทิศทาง A<->B)"""
    stmt = select(CourseEquivalency).where(
        (CourseEquivalency.course_code_a == course_code) | (CourseEquivalency.course_code_b == course_code)
    )
    equivalencies = session.scalars(stmt).all()
    results = []
    for eq in equivalencies:
        other_code = eq.course_code_b if eq.course_code_a == course_code else eq.course_code_a
        other_course = session.get(Course, other_code)
        if other_course:
            results.append(other_course)
    return results


def delete_course_equivalency(session: Session, equivalency_id: int) -> bool:
    equivalency = session.get(CourseEquivalency, equivalency_id)
    if equivalency is None:
        return False
    session.delete(equivalency)
    session.commit()
    return True


# ===========================================================================
# ElectiveTermSlot (จำนวนช่องวิชาเลือกต่อหมวด ต่อเทอม ต่อแผนทางเลือก)
# ===========================================================================

def set_elective_term_slot(
    session: Session, curriculum_id: int, group_id: int, year: int, semester: int,
    slot_count: int = 1, study_plan_id: Optional[int] = None,
) -> ElectiveTermSlot:
    """สร้างใหม่ถ้ายังไม่มี หรืออัปเดตถ้ามีอยู่แล้ว (upsert ตาม curriculum+group+plan+ปี+เทอม)"""
    stmt = select(ElectiveTermSlot).where(
        ElectiveTermSlot.curriculum_id == curriculum_id,
        ElectiveTermSlot.group_id == group_id,
        ElectiveTermSlot.study_plan_id == study_plan_id,
        ElectiveTermSlot.year == year,
        ElectiveTermSlot.semester == semester,
    )
    slot = session.scalars(stmt).first()
    if slot is None:
        slot = ElectiveTermSlot(
            curriculum_id=curriculum_id, group_id=group_id, study_plan_id=study_plan_id,
            year=year, semester=semester, slot_count=slot_count,
        )
        session.add(slot)
    else:
        slot.slot_count = slot_count
    session.commit()
    session.refresh(slot)
    return slot


def list_elective_term_slots(
    session: Session, curriculum_id: int, study_plan_id: Optional[int] = None,
    include_shared: bool = True,
) -> List[ElectiveTermSlot]:
    """
    study_plan_id=None -> คืนเฉพาะช่องที่ใช้ร่วมกันทุกแผน (study_plan_id IS NULL)
    study_plan_id=<id> -> คืนช่องของแผนนั้น + ช่องที่ใช้ร่วมกันทุกแผน (ถ้า include_shared=True)
    """
    stmt = select(ElectiveTermSlot).where(ElectiveTermSlot.curriculum_id == curriculum_id)
    if study_plan_id is None:
        stmt = stmt.where(ElectiveTermSlot.study_plan_id.is_(None))
    elif include_shared:
        stmt = stmt.where(
            (ElectiveTermSlot.study_plan_id == study_plan_id) | (ElectiveTermSlot.study_plan_id.is_(None))
        )
    else:
        stmt = stmt.where(ElectiveTermSlot.study_plan_id == study_plan_id)
    return list(session.scalars(stmt).all())


def delete_elective_term_slot(session: Session, slot_id: int) -> bool:
    slot = session.get(ElectiveTermSlot, slot_id)
    if slot is None:
        return False
    session.delete(slot)
    session.commit()
    return True


# ===========================================================================
# CourseGrade (ผลการเรียนรายวิชา — เก็บแบบผู้ใช้คนเดียว ยังไม่รองรับหลายนักศึกษา)
# ===========================================================================

def set_course_grade(
    session: Session, curriculum_id: int, course_code: str, grade: str,
    actual_year: Optional[int] = None, actual_semester: Optional[int] = None,
) -> CourseGrade:
    """บันทึกเกรด (สร้างใหม่ถ้ายังไม่มี หรืออัปเดตถ้ามีอยู่แล้ว upsert ตาม curriculum+course)"""
    stmt = select(CourseGrade).where(
        CourseGrade.curriculum_id == curriculum_id, CourseGrade.course_code == course_code,
    )
    record = session.scalars(stmt).first()
    if record is None:
        record = CourseGrade(
            curriculum_id=curriculum_id, course_code=course_code, grade=grade,
            actual_year=actual_year, actual_semester=actual_semester,
        )
        session.add(record)
    else:
        record.grade = grade
        record.actual_year = actual_year
        record.actual_semester = actual_semester
    session.commit()
    session.refresh(record)
    return record


def list_course_grades(session: Session, curriculum_id: int) -> List[CourseGrade]:
    stmt = select(CourseGrade).where(CourseGrade.curriculum_id == curriculum_id)
    return list(session.scalars(stmt).all())


def delete_course_grade(session: Session, grade_id: int) -> bool:
    record = session.get(CourseGrade, grade_id)
    if record is None:
        return False
    session.delete(record)
    session.commit()
    return True


# ===========================================================================
# Query ระดับสูง (รวมหลายตาราง) — ใช้สำหรับหน้าจอสรุปผล/ตรวจสอบเงื่อนไขจบ
# ===========================================================================

def get_group_tree(session: Session, curriculum_id: Optional[int] = None) -> List[Dict]:
    """
    คืนโครงสร้างหมวดวิชาแบบ tree (หมวดใหญ่ -> หมวดย่อย) พร้อมรายวิชาในแต่ละหมวดย่อย
    curriculum_id=None -> เฉพาะหมวด GenEd กลาง / ระบุ -> หมวดของหลักสูตรนั้น + GenEd กลาง
    """
    top_groups = list_course_groups(session, curriculum_id=curriculum_id, top_level_only=True)

    def build_node(group: CourseGroup) -> Dict:
        children = get_group_children(session, group.id)
        courses = list_courses_for_curriculum(session, curriculum_id, group_id=group.id) if curriculum_id else []
        return {
            "id": group.id,
            "name": group.name,
            "group_type": group.group_type.value,
            "children": [build_node(child) for child in children],
            "courses": [
                {"code": link.course_code, "is_required": link.is_required,
                 "recommended_year": link.recommended_year, "recommended_semester": link.recommended_semester}
                for link in courses
            ],
        }

    return [build_node(g) for g in top_groups]


def check_graduation_progress(
    session: Session, curriculum_id: int, completed_course_codes: List[str],
    study_plan_id: Optional[int] = None,
) -> Dict:
    """
    ตรวจสอบความคืบหน้าการจบการศึกษาของนักศึกษา 1 คน เทียบกับเงื่อนไขของหลักสูตร

    completed_course_codes: รายการรหัสวิชาที่นักศึกษาสอบผ่านแล้วทั้งหมด
    study_plan_id: ถ้าหลักสูตรมีแผนทางเลือก (เช่น โครงงาน/สหกิจ) ระบุแผนที่นักศึกษาเลือก

    คืนค่า dict สรุปหน่วยกิตที่ได้/ต้องการต่อหมวด รวมถึงหมวดเลือกเสรี (นับวิชาที่เหลือทั้งหมด)
    และคำนวณรวมวิชาที่เทียบเคียงกันได้ (CourseEquivalency) ให้อัตโนมัติ
    """
    completed = set(completed_course_codes)
    # ขยายชุดวิชาที่ผ่านแล้ว ด้วยวิชาที่เทียบเคียงกันได้ (FULL เท่านั้น นับเป็นวิชาเดียวกัน)
    expanded = set(completed)
    for code in completed:
        for equivalent in find_equivalent_courses(session, code):
            expanded.add(equivalent.code)

    requirements = list_group_requirements(session, curriculum_id)
    used_codes: set = set()
    result_groups = []

    for req in requirements:
        group = session.get(CourseGroup, req.group_id)
        if group.group_type == GroupType.FREE_ELECTIVE:
            # เลือกเสรี: ไม่ต้องมี CurriculumCourse ผูกไว้ล่วงหน้า คำนวณทีหลังจากวิชาที่เหลือ
            result_groups.append({
                "group_id": group.id, "group_name": group.name,
                "group_type": group.group_type.value,
                "min_credits": req.min_credits, "earned_credits": None,  # คำนวณหลังวนครบทุกหมวด
                "is_free_elective": True,
            })
            continue

        links = list_courses_for_curriculum(
            session, curriculum_id, group_id=req.group_id, study_plan_id=study_plan_id,
        )
        earned = 0
        for link in links:
            if link.course_code in expanded:
                course = session.get(Course, link.course_code)
                earned += course.credits if course else 0
                used_codes.add(link.course_code)
        result_groups.append({
            "group_id": group.id, "group_name": group.name,
            "group_type": group.group_type.value,
            "min_credits": req.min_credits, "earned_credits": earned,
            "is_met": earned >= req.min_credits,
            "is_free_elective": False,
        })

    # คำนวณหมวดเลือกเสรี: วิชาที่ผ่านแล้วแต่ยังไม่ถูกนับในหมวดใดเลย
    # เช็คทั้งรหัสวิชาที่ผ่านเอง และคู่เทียบของมัน — ถ้าตัวใดตัวหนึ่งถูกนับในหมวดอื่นไปแล้ว (used_codes)
    # ถือว่าวิชานี้ถูกใช้ไปแล้ว ไม่ต้องนับเป็นเลือกเสรีซ้ำอีก (ไม่ว่าจะผ่านวิชาต้นฉบับ หรือผ่านคู่เทียบของมัน)
    leftover_credits = 0
    for code in completed:
        related_codes = {code} | {e.code for e in find_equivalent_courses(session, code)}
        if related_codes & used_codes:
            continue
        course = session.get(Course, code)
        if course:
            leftover_credits += course.credits

    for g in result_groups:
        if g["is_free_elective"]:
            g["earned_credits"] = leftover_credits
            g["is_met"] = leftover_credits >= g["min_credits"]

    total_required = sum(g["min_credits"] for g in result_groups)
    total_earned = sum(min(g["earned_credits"], g["min_credits"]) for g in result_groups)  # ตัดหน่วยกิตเกินโควตาต่อหมวด

    return {
        "curriculum_id": curriculum_id,
        "groups": result_groups,
        "total_required_credits": total_required,
        "total_earned_credits": total_earned,
        "is_graduated": all(g["is_met"] for g in result_groups),
    }
