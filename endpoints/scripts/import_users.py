import csv
from flask import Blueprint
from flask import make_response, request
import json
from models import User, Section, Enrollment
from models import db
from datetime import datetime

scripts_blueprint = Blueprint('scripts_blueprint', __name__)

@scripts_blueprint.route('/create_sections', methods=["POST"])
def create_sections():
    try:
        file_path = 'assets\\Smart Classroom Data Source - FormattedSection.csv'
        machine_id = 1
        with open(file_path, 'r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            headers = next(reader)
            for row in reader:
                section_name, teacher_name, start_time, end_time, students = row
                print(f"Section: {section_name}")
                print(f"Teacher: {teacher_name}")
                print(f"Start Time: {start_time}")
                print(f"End Time: {end_time}")
                print(f"Students: {students.split(';')}")
                teacher = User.query.filter(User.fullname == teacher_name).first()
                if teacher is None:
                    print("No teacher found for", teacher_name)
                else:
                    print("Teacher found:", teacher.id)
                section = Section(
                    name = section_name,
                    start_time = datetime.strptime(start_time, '%H:%M'),
                    end_time =  datetime.strptime(end_time, '%H:%M'),
                    teacher_id = teacher.id,
                    machine_id = machine_id
                )
                db.session.add(section)
                db.session.commit()
                section_instance = Section.query.filter(Section.name == section_name).first()
                for student in students.split(";"):
                    student_instance = User.query.filter(User.fullname == student).first()
                    if student_instance is None:
                        print("Student not found", student)
                    enrollment = Enrollment(
                        section_id = section_instance.id,
                        student_id = student_instance.id
                    )
                    db.session.add(enrollment)
                    db.session.commit()
                
                
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        return make_response({"status": 200, "remarks": "Success"})
    

@scripts_blueprint.route('/create_users', methods=["POST"])
def create_users():
    try:
        file_path = 'assets\\Smart Classroom Data Source - Users.csv'
        with open(file_path, 'r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            headers = next(reader)
            teacher_count = 1
            student_count = 1
            for row in reader:
                name, user_type, code = row
                print(f"Name: {name}")
                print(f"User Type: {user_type}")
                print(f"Code: {code}")
                if user_type.lower() == "teacher":
                    username = f"teacher{teacher_count}"
                    password = "teacherpass123"
                    teacher_count += 1
                else:
                    username = f"student{student_count}"
                    password = "studentpass123"
                    student_count += 1
                user = User(
                    username = username,
                    password = password,
                    fullname = name,
                    user_type = user_type,
                    code = code
                )
                db.session.add(user)
                db.session.commit()

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        return make_response({"status": 200, "remarks": "Success"})
