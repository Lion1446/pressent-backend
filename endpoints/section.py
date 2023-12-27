from flask import Blueprint
from flask import make_response, request
import json
from models import Section
from models import db
from datetime import datetime


section_blueprint = Blueprint('section_blueprint', __name__)

@section_blueprint.route('/section', methods=["POST", "GET", "PATCH", "DELETE"])
def section():
    try:
        if request.method == "POST":
            request_data = request.data
            request_data = json.loads(request_data.decode('utf-8')) 
            query = Section.query.filter(
                Section.name == request_data["name"],
                Section.teacher_id == request_data["teacher_id"],
                Section.machine_id == request_data["machine_id"],
                ).all()
            if query:
                resp = make_response({"status": 400, "remarks": "Section already exists."})
            else:
                instance = Section(
                    name = request_data["name"],
                    start_time = datetime.strptime(request_data["start_time"], "%m/%d/%Y %H:%M:%S"),
                    end_time = datetime.strptime(request_data["end_time"], "%m/%d/%Y %H:%M:%S"),
                    teacher_id = request_data["teacher_id"],
                    machine_id = request_data["machine_id"]
                )
                db.session.add(instance)
                db.session.commit()
                resp = make_response({"status": 200, "remarks": "Success"})
        elif request.method == "GET":
            id = request.args.get('id')
            if id is None:
                resp = make_response({"status": 400, "remarks": "Missing id in the query string"})
            else:
                instance = Section.query.get(id)
                if instance:
                    response_body = instance.to_map()
                    response_body["status"] = 200
                    response_body["remarks"] = "Success"
                else:
                    response_body = {}
                    response_body["status"] = 404
                    response_body["remarks"] = "Section does not exist"
                resp = make_response(response_body)
        elif request.method == "PATCH":
            id = request.args.get('id')
            if id is None:
                resp = make_response({"status": 400, "remarks": "Missing id in the query string"})
            section = Section.query.get(id)      
            if section is None:
                return make_response({"status": 404, "remarks": "Section not found"})
            request_data = request.data
            request_data = json.loads(request_data.decode('utf-8')) 
            section.name = request_data["name"]
            section.start_time = datetime.strptime(request_data["start_time"], "%m/%d/%Y %H:%M:%S")
            section.end_time = datetime.strptime(request_data["end_time"], "%m/%d/%Y %H:%M:%S")
            section.teacher_id = request_data["teacher_id"]
            section.machine_id = request_data["machine_id"]
            db.session.commit()
            return make_response({"status": 200, "remarks": "Success"})
        elif request.method == "DELETE":
            id = request.args.get('id')
            instance = Section.query.get(id)
            if instance is None:
                resp = make_response({"status": 404, "remarks": "Section does not exist."})
            else:
                db.session.delete(instance)
                db.session.commit()
                resp = make_response({"status": 200, "remarks": "Success"})
    except Exception as e:
        print(e)
        resp = make_response({"status": 500, "remarks": f"Internal server error: {e}"})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
    
@section_blueprint.route('/sections', methods=["GET"])
def sections():
    try:
        teacher_id = request.args.get('teacher_id')
        if teacher_id is None:
            resp = make_response({"status": 400, "remarks": "Missing teacher_id in the query string"})
        else:
            instances = Section.query.filter(Section.teacher_id == teacher_id).all()
            sections = []
            for instance in instances:
                sections.append(instance.to_map())
            response_body = {
                "status": 200,
                "remarks": "Success",
                "data": sections
            }
            resp = make_response(response_body)
    except Exception as e:
        print(e)
        resp = make_response({"status": 500, "remarks": f"Internal server error: {e}"})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp