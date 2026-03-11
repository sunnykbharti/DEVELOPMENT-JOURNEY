from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Course(db.Model) :
    course_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    course_name = db.Column(db.String(50), nullable = False)
    course_code = db.Column(db.String(50), unique = True, nullable = False)
    course_description = db.Column(db.String(200))

class Student(db.Model) : 
    student_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    roll_number = db.Column(db.String(50), unique = True, nullable = False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100))

class Enrollment(db.Model) : 
    enrollment_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    student_id = db.Column(db.ForeignKey('Student.student_id'), nullable = False)
    course_id = db.Column(db.ForeignKey('Course.course_id'), nullable = False)

