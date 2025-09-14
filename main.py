import argparse
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from models import Student, Group, Teacher, Subject
from database import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def create_record(model, **kwargs):
    if model == 'Teacher':
        record = Teacher(fullname=kwargs.get('name'))
    elif model == 'Group':
        record = Group(name=kwargs.get('name'))
    elif model == 'Student':
        record = Student(fullname=kwargs.get('name'), group_id=kwargs.get('group_id'))
    elif model == 'Subject':
        record = Subject(name=kwargs.get('name'), teacher_id=kwargs.get('teacher_id'))
    else:
        return "Invalid model specified."

    session.add(record)
    session.commit()
    return f"{model} created successfully."


def list_records(model):
    if model == 'Teacher':
        records = session.query(Teacher).all()
    elif model == 'Group':
        records = session.query(Group).all()
    elif model == 'Student':
        records = session.query(Student).all()
    elif model == 'Subject':
        records = session.query(Subject).all()
    else:
        return "Invalid model specified."

    for record in records:
        if hasattr(record, 'name'):
            print(f"ID: {record.id}, Name: {record.name}")
        if hasattr(record, 'fullname'):
            print(f"ID: {record.id}, Fullname: {record.fullname}")
    return "List operation finished."


def update_record(model, id, **kwargs):
    if model == 'Teacher':
        record = session.query(Teacher).filter_by(id=id).first()
        if record and kwargs.get('name'):
            record.fullname = kwargs.get('name')
    elif model == 'Group':
        record = session.query(Group).filter_by(id=id).first()
        if record and kwargs.get('name'):
            record.name = kwargs.get('name')
    else:
        return "Invalid model specified or record not found."

    session.commit()
    return f"{model} with id {id} updated."


def remove_record(model, id):
    if model == 'Teacher':
        record = session.query(Teacher).filter_by(id=id).first()
    elif model == 'Group':
        record = session.query(Group).filter_by(id=id).first()
    else:
        return "Invalid model specified."

    if record:
        session.delete(record)
        session.commit()
        return f"{model} with id {id} removed."
    return "Record not found."


def main():
    parser = argparse.ArgumentParser(description="CLI for CRUD operations on the database.")
    parser.add_argument("-a", "--action", choices=['create', 'list', 'update', 'remove'], required=True,
                        help="CRUD action")
    parser.add_argument("-m", "--model", choices=['Teacher', 'Group', 'Student', 'Subject'], required=True,
                        help="Model to perform action on")
    parser.add_argument("--id", type=int, help="ID of the record for update/remove")
    parser.add_argument("-n", "--name", type=str, help="Name or fullname for create/update")
    parser.add_argument("--group_id", type=int, help="Group ID for student")
    parser.add_argument("--teacher_id", type=int, help="Teacher ID for subject")

    args = parser.parse_args()

    if args.action == 'create':
        print(create_record(model=args.model, name=args.name, group_id=args.group_id, teacher_id=args.teacher_id))
    elif args.action == 'list':
        print(list_records(model=args.model))
    elif args.action == 'update':
        if args.id and args.name:
            print(update_record(model=args.model, id=args.id, name=args.name))
        else:
            print("For update action, --id and --name are required.")
    elif args.action == 'remove':
        if args.id:
            print(remove_record(model=args.model, id=args.id))
        else:
            print("For remove action, --id is required.")

    session.close()


if __name__ == '__main__':
    main()
