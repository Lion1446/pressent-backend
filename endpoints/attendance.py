from flask import Blueprint
from flask import make_response, request
import json
from models import Attendance, Section, User
from models import db
from datetime import datetime, timedelta


attendance_blueprint = Blueprint('attendance_blueprint', __name__)

@attendance_blueprint.route('/attendance', methods=["POST", "GET", "DELETE"])
def attendance():
    try:
        if request.method == "POST":
            request_data = request.data
            request_data = json.loads(request_data.decode('utf-8')) 
            request_data["code"] = request_data["code"].upper()
            print(request_data)
            logged_time = datetime.now()
            section = Section.query.filter(Section.name == request_data["section_name"]).first()
            if section is None:
                return make_response({"status": 404, "remarks": "Inappropriate log info"})
            student = User.query.filter(User.code == request_data["code"], User.user_type == 1).first()
            if student is None:
                return make_response({"status": 404, "remarks": "Student not found in the database"})
            response_body = {}
            response_body["remarks"] = []
            instance = Attendance(
                student_id = student.id,
                section_id = section.id,
                datetime_created = logged_time
            )
            db.session.add(instance)
            db.session.commit()
            response_body["status"] = 200
            response_body["remarks"] = "Succes" 
            resp = make_response({"status": 200, "remarks": "Success"})

        elif request.method == "GET":
            section_id = request.args.get('section_id')
            date = request.args.get('date')
            if section_id is None or date is None:
                resp = make_response({"status": 400, "remarks": "Missing id or date in the query string"})
            else:
                section = Section.query.get(section_id)
                date = datetime.strptime(date, '%m/%d/%Y')
                attendance = Attendance.query.filter(
                    Attendance.section_id == section_id,
                    Attendance.datetime_created >= date,
                    Attendance.datetime_created < date + timedelta(days=1)
                ).all()
                students = []
                for a in attendance:
                    student = User.query.filter(User.id == a.student_id, User.user_type == 1).first()
                    log = a.to_map()
                    log["student"] = student.fullname
                    students.append(log)
                response_body = {}
                response_body["status"] = 200
                response_body["remarks"] = "Success"
                response_body["attendance"] = students
                resp = make_response(response_body)
        elif request.method == "DELETE":
            id = request.args.get('id')
            instance = Attendance.query.get(id)
            if instance is None:
                resp = make_response({"status": 404, "remarks": "Attendance does not exist."})
            else:
                db.session.delete(instance)
                db.session.commit()
                resp = make_response({"status": 200, "remarks": "Success"})
    except Exception as e:
        print(e)
        resp = make_response({"status": 500, "remarks": f"Internal server error: {e}"})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp