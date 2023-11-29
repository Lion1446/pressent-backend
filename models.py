from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    datetime_created = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(hours=8))
    datetime_deleted = db.Column(db.DateTime, default=None, nullable=True)

    def to_map(self):
        return {
            "id": self.id,
            "datetime_created": self.datetime_created,
            "datetime_deleted": self.datetime_deleted
        }
    

class User(BaseModel):
    __tablename__ = "user"
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    fullname = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.Integer, nullable=False)
    code = db.Column(db.String(100), nullable=False)

    def to_map(self):
        user_data = super().to_map()
        user_data["username"] = self.username
        user_data["password"] = self.password
        user_data["fullname"] = self.fullname
        user_data["user_type"] = self.user_type
        user_data["code"] = self.code
        return user_data
    
class Section(BaseModel):
    __tablename__ = "section"
    name = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    teacher_id = db.Column(db.Integer, nullable=False)
    machine_id = db.Column(db.String(100), nullable=False)

    def to_map(self):
        section_data = super().to_map()
        section_data["name"] = self.name
        section_data["start_time"] = self.start_time
        section_data["end_time"] = self.end_time
        section_data["teacher_id"] = self.teacher_id
        section_data["machine_id"] = self.machine_id
        return section_data
    
class Enrollment(BaseModel):
    __tablename__ = "enrollment"
    section_id = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, nullable=False)

    def to_map(self):
        enrollment_data = super().to_map()
        enrollment_data["section_id"] = self.section_id
        enrollment_data["student_id"] = self.student_id
        return enrollment_data
    
class Attendance(BaseModel):
    __tablename__ = "attendance"
    section_id = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, nullable=False)

    def to_map(self):
        attendance_data = super().to_map()
        attendance_data["section_id"] = self.section_id
        attendance_data["student_id"] = self.student_id
        return attendance_data