from flask import Blueprint
from flask import make_response, request
import json
from models import Enrollment, Section, User
from models import db
from datetime import datetime


enrollment_blueprint = Blueprint('enrollment_blueprint', __name__)

@enrollment_blueprint.route('/enrollment', methods=["POST", "GET", "DELETE"])
def enrollment():
    try:
        if request.method == "POST":
            request_data = request.data
            request_data = json.loads(request_data.decode('utf-8')) 
            section = Section.query.get(request_data["section_id"])
            student = User.query.filter(User.id == request_data["student_id"], User.user_type == 1).first()
            response_body = {}
            response_body["remarks"] = []
            if section and student:
                instance = Enrollment(
                    student_id = request_data["student_id"],
                    section_id = request_data["section_id"]
                )
                db.session.add(instance)
                db.session.commit()
                response_body["status"] = 200
                response_body["remarks"] = "Succes" 
                resp = make_response({"status": 200, "remarks": "Success"})
            else:
                response_body["remarks"].append("Student or section does not exists.")
                response_body["status"] = 404
                return make_response(response_body)
        elif request.method == "GET":
            section_id = request.args.get('section_id')
            if section_id is None:
                resp = make_response({"status": 400, "remarks": "Missing id in the query string"})
            else:
                section = Section.query.get(section_id)
                enrollment = Enrollment.query.filter(Enrollment.section_id == section_id).all()
                students = []
                for e in enrollment:
                    student = User.query.filter(User.id == e.student_id, User.user_type == 1).first()
                    if student:
                        students.append(student.to_map())
                teacher = User.query.filter(User.id == section.teacher_id, User.user_type == 2).first()
                response_body = {}
                response_body["status"] = 200
                response_body["remarks"] = "Success"
                response_body["students"] = students
                response_body["section"] = section.to_map()
                response_body["teacher"] = teacher.to_map()
                resp = make_response(response_body)
        elif request.method == "DELETE":
            section_id = request.args.get('section_id')
            instance = Enrollment.query.get(section_id)
            if instance is None:
                resp = make_response({"status": 404, "remarks": "Enrollment does not exist."})
            else:
                db.session.delete(instance)
                db.session.commit()
                resp = make_response({"status": 200, "remarks": "Success"})
    except Exception as e:
        print(e)
        resp = make_response({"status": 500, "remarks": f"Internal server error: {e}"})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp