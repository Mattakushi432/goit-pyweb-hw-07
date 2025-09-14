from faker import Faker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import random
from datetime import date

from models import Student, Group, Teacher, Subject, Grade
from database import DATABASE_URL, Base

NUM_STUDENTS = 40
NUM_GROUPS = 3
NUM_TEACHERS = 4
NUM_SUBJECTS = 7
MAX_GRADES_PER_STUDENT = 20

fake = Faker()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def seed_data():
    # Ensure tables exist; for SQLite/dev runs without explicit Alembic migrations
    Base.metadata.create_all(bind=engine)
    try:
        groups = [Group(name=fake.word().capitalize()) for _ in range(NUM_GROUPS)]
        session.add_all(groups)
        session.commit()

        teachers = [Teacher(fullname=fake.name()) for _ in range(NUM_TEACHERS)]
        session.add_all(teachers)
        session.commit()

        subjects = [Subject(name=fake.catch_phrase(), teacher_id=random.choice(teachers).id) for _ in
                    range(NUM_SUBJECTS)]
        session.add_all(subjects)
        session.commit()

        students = [Student(fullname=fake.name(), group_id=random.choice(groups).id) for _ in range(NUM_STUDENTS)]
        session.add_all(students)
        session.commit()

        # Створення оцінок
        for student in students:
            num_grades = random.randint(5, MAX_GRADES_PER_STUDENT)
            for _ in range(num_grades):
                grade = Grade(
                    grade=random.randint(1, 12),
                    date_of=fake.date_between(start_date='-1y', end_date='today'),
                    student_id=student.id,
                    subject_id=random.choice(subjects).id
                )
                session.add(grade)
        session.commit()
        print("The database is successfully filled with data.")
    except Exception as e:
        session.rollback()
        print(f"Error while filling in the database: {e}")
    finally:
        session.close()


if __name__ == '__main__':
    seed_data()
