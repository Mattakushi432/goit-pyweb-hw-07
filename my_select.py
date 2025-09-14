from sqlalchemy import func, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from models import Student, Group, Teacher, Subject, Grade
from database import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def select_1():
    """Find the 5 students with the highest average score in all subjects."""
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
    return result


def select_2(subject_name):
    """Find the student with the highest grade point average in a particular subject."""
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade).join(Student).join(Subject).filter(Subject.name == subject_name) \
        .group_by(Student.id).order_by(desc('avg_grade')).first()
    return result


def select_3(subject_name):
    """Find the average score in groups for a particular subject."""
    result = session.query(Group.name, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade).join(Student).join(Group).join(Subject).filter(Subject.name == subject_name) \
        .group_by(Group.name).order_by(desc('avg_grade')).all()
    return result


def select_4():
    """Find the average score in the stream (across the entire grade table)."""
    result = session.query(func.round(func.avg(Grade.grade), 2)).scalar()
    return result


def select_5(teacher_name):
    """Find which courses a particular teacher teaches."""
    result = session.query(Subject.name).join(Teacher).filter(Teacher.fullname == teacher_name).all()
    return [row[0] for row in result]


def select_6(group_name):
    """Find a list of students in a specific group."""
    result = session.query(Student.fullname).join(Group).filter(Group.name == group_name).all()
    return [row[0] for row in result]


def select_7(group_name, subject_name):
    """Find the grades of students in a particular group in a particular subject."""
    result = session.query(Student.fullname, Grade.grade) \
        .select_from(Grade).join(Student).join(Group).join(Subject) \
        .filter(Group.name == group_name, Subject.name == subject_name).all()
    return result


def select_8(teacher_name):
    """Find the average grade that a particular teacher gives in his subjects."""
    result = session.query(func.round(func.avg(Grade.grade), 2)) \
        .select_from(Grade).join(Subject).join(Teacher) \
        .filter(Teacher.fullname == teacher_name).scalar()
    return result


def select_9(student_name):
    """Find a list of courses taken by a particular student."""
    result = session.query(func.distinct(Subject.name)) \
        .select_from(Grade).join(Subject).join(Student) \
        .filter(Student.fullname == student_name).all()
    return [row[0] for row in result]


def select_10(student_name, teacher_name):
    """A list of courses taught by a certain teacher to a certain student."""
    result = session.query(func.distinct(Subject.name)) \
        .select_from(Grade).join(Subject).join(Teacher).join(Student) \
        .filter(Student.fullname == student_name, Teacher.fullname == teacher_name).all()
    return [row[0] for row in result]


if __name__ == '__main__':
    print("Select 1: 5 students with the highest grade point average:")
    print(select_1())

    print("\nSelect 2: the student with the highest grade point average from 'Catchy Phrase':")
    first_subject = session.query(Subject).first()
    if first_subject:
        print(select_2(first_subject.name))

    print("\nSelect 3: Average score in groups in the same subject:")
    if first_subject:
        print(select_3(first_subject.name))

    print("\nSelect 4: Average score in the course:")
    print(select_4())

    first_teacher = session.query(Teacher).first()
    if first_teacher:
        print(f"\nSelect 5: Teacher's courses '{first_teacher.fullname}':")
        print(select_5(first_teacher.fullname))

    first_group = session.query(Group).first()
    if first_group:
        print(f"\nSelect 6: Students in the group '{first_group.name}':")
        print(select_6(first_group.name))

    if first_group and first_subject:
        print(f"\nSelect 7: Grades of students in group ‘{first_group.name}’ in subject ‘{first_subject.name}’:")
        print(select_7(first_group.name, first_subject.name))

    if first_teacher:
        print(f"\nSelect 8: Average grade point average of the teacher '{first_teacher.fullname}':")
        print(select_8(first_teacher.fullname))

    first_student = session.query(Student).first()
    if first_student:
        print(f"\nSelect 9: Courses attended by '{first_student.fullname}':")
        print(select_9(first_student.fullname))

    if first_student and first_teacher:
        print(f"\nSelect 10: Courses that ‘{first_student.fullname}’ is taking with ‘{first_teacher.fullname}’:")
        print(select_10(first_student.fullname, first_teacher.fullname))
