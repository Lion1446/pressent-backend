from flask import Flask, make_response
from models import *
import os
from endpoints.login import login_blueprint
from endpoints.user import user_blueprint
from endpoints.section import section_blueprint
from endpoints.enrollment import enrollment_blueprint
from endpoints.attendance import attendance_blueprint
from endpoints.scripts.import_users import scripts_blueprint


## ======================= STARTUPS =================================
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()  

app.register_blueprint(login_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(section_blueprint)
app.register_blueprint(enrollment_blueprint)
app.register_blueprint(attendance_blueprint)
app.register_blueprint(scripts_blueprint)


## ======================= ENDPOINTS =================================

@app.route('/')
def index():
    return make_response({"status": 200, "remarks": "Backend connected"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)