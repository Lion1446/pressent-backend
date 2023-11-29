from flask import Blueprint
from flask import make_response, request
import json
from models import User
from models import db

user_blueprint = Blueprint('user_blueprint', __name__)

@user_blueprint.route('/user', methods=["POST", "GET", "PATCH", "DELETE"])
def user():
    try:
        if request.method == "POST":
            request_data = request.data
            request_data = json.loads(request_data.decode('utf-8')) 
            query = User.query.filter(
                User.username == request_data["username"],
                User.password == request_data["password"],
                User.fullname == request_data["fullname"],
                User.user_type == request_data["user_type"],
                User.code == request_data["code"],
                ).all()
            if query:
                resp = make_response({"status": 400, "remarks": "User already exists."})
            else:
                instance = User(
                    username = request_data["username"],
                    password = request_data["password"],
                    fullname = request_data["fullname"],
                    user_type = request_data["user_type"],
                    code = request_data["code"]
                )
                db.session.add(instance)
                db.session.commit()
                resp = make_response({"status": 200, "remarks": "Success"})
        elif request.method == "GET":
            id = request.args.get('id')
            if id is None:
                resp = make_response({"status": 400, "remarks": "Missing id in the query string"})
            else:
                instance = User.query.get(id)
                if instance:
                    response_body = instance.to_map()
                    response_body["status"] = 200
                    response_body["remarks"] = "Success"
                else:
                    response_body = {}
                    response_body["status"] = 404
                    response_body["remarks"] = "User does not exist"
                resp = make_response(response_body)
        elif request.method == "PATCH":
            id = request.args.get('id')
            if id is None:
                resp = make_response({"status": 400, "remarks": "Missing id in the query string"})
            user = User. query.get(id)      
            if user is None:
                return make_response({"status": 404, "remarks": "User not found"})
            request_data = request.data
            request_data = json.loads(request_data.decode('utf-8')) 
            user.password = request_data["password"]
            user.fullname = request_data["fullname"]
            user.code = request_data["code"]
            user.user_type = request_data["user_type"]
            db.session.commit()
            return make_response({"status": 200, "remarks": "Success"})
        elif request.method == "DELETE":
            id = request.args.get('id')
            instance = User.query.get(id)
            if instance is None:
                resp = make_response({"status": 404, "remarks": "User does not exist."})
            else:
                db.session.delete(instance)
                db.session.commit()
                resp = make_response({"status": 200, "remarks": "Success"})
    except Exception as e:
        print(e)
        resp = make_response({"status": 500, "remarks": f"Internal server error: {e}"})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp