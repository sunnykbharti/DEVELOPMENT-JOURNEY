from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with

# --- App, DB, and API Initialization ---
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api_database.sqlite3'
db = SQLAlchemy(app)
api = Api(app)


# --- Database Models ---

class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name = db.Column(db.String, nullable=False)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_description = db.Column(db.String)

class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)
    enrollments = db.relationship('Enrollment', backref='student', lazy=True)

class Enrollment(db.Model):
    __tablename__ = 'enrollment'
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)


# --- Request Parsers ---

# Course parsers
course_post_parser = reqparse.RequestParser()
course_post_parser.add_argument('course_name', type=str, required=True, help="Course Name is required (COURSE001)")
course_post_parser.add_argument('course_code', type=str, required=True, help="Course Code is required (COURSE002)")
course_post_parser.add_argument('course_description', type=str)

course_put_parser = reqparse.RequestParser()
course_put_parser.add_argument('course_name', type=str)
course_put_parser.add_argument('course_code', type=str)
course_put_parser.add_argument('course_description', type=str)

# Student parsers
student_post_parser = reqparse.RequestParser()
student_post_parser.add_argument('roll_number', type=str, required=True, help="Roll Number required (STUDENT001)")
student_post_parser.add_argument('first_name', type=str, required=True, help="First Name is required (STUDENT002)")
student_post_parser.add_argument('last_name', type=str)

student_put_parser = reqparse.RequestParser()
student_put_parser.add_argument('roll_number', type=str)
student_put_parser.add_argument('first_name', type=str)
student_put_parser.add_argument('last_name', type=str)

# --- NEW: Enrollment Parser ---
enrollment_post_parser = reqparse.RequestParser()
enrollment_post_parser.add_argument('course_id', type=int, required=True, help="Course ID is required for enrollment")


# --- Response Formatting ---

# Course fields
course_fields = {
    'course_id': fields.Integer,
    'course_name': fields.String,
    'course_code': fields.String,
    'course_description': fields.String
}

# Student fields
student_fields = {
    'student_id': fields.Integer,
    'roll_number': fields.String,
    'first_name': fields.String,
    'last_name': fields.String
}

# --- NEW: Enrollment Fields ---
enrollment_fields = {
    'enrollment_id': fields.Integer,
    'student_id': fields.Integer,
    'course_id': fields.Integer
}


# --- Course API Resources ---

class CourseAPI(Resource):
    @marshal_with(course_fields)
    def get(self, course_id):
        course = Course.query.get(course_id)
        if not course:
            abort(404, message="Course not found")
        return course

    @marshal_with(course_fields)
    def put(self, course_id):
        course = Course.query.get(course_id)
        if not course:
            abort(404, message="Course not found")
        
        args = course_put_parser.parse_args()
        
        if not any(args.values()):
             abort(400, error_code="COURSE_UPDATE001", error_message="No fields to update")

        if args['course_name']:
            course.course_name = args['course_name']
        if args['course_code']:
            existing_course = Course.query.filter_by(course_code=args['course_code']).first()
            if existing_course and existing_course.course_id != course_id:
                abort(409, message="course_code already exists")
            course.course_code = args['course_code']
        if args['course_description']:
            course.course_description = args['course_description']
            
        db.session.commit()
        return course, 200

    def delete(self, course_id):
        course = Course.query.get(course_id)
        if not course:
            abort(404, message="Course not found")
            
        db.session.delete(course)
        db.session.commit()
        return {"message": "Successfully Deleted"}, 200

class CourseListAPI(Resource):
    @marshal_with(course_fields)
    def post(self):
        args = course_post_parser.parse_args()
        
        if not args.get('course_name'):
            return {"error_code": "COURSE001", "error_message": "Course Name is required"}, 400
        if not args.get('course_code'):
            return {"error_code": "COURSE002", "error_message": "Course Code is required"}, 400

        if Course.query.filter_by(course_code=args['course_code']).first():
            abort(409, message="course_code already exist")
            
        new_course = Course(
            course_name=args['course_name'],
            course_code=args['course_code'],
            course_description=args['course_description']
        )
        db.session.add(new_course)
        db.session.commit()
        return new_course, 201


# --- Student API Resources ---

class StudentAPI(Resource):
    @marshal_with(student_fields)
    def get(self, student_id):
        student = Student.query.get(student_id)
        if not student:
            abort(404, message="Student not found")
        return student

    @marshal_with(student_fields)
    def put(self, student_id):
        student = Student.query.get(student_id)
        if not student:
            abort(404, message="Student not found")
            
        args = student_put_parser.parse_args()

        if not any(args.values()):
             abort(400, error_code="STUDENT_UPDATE001", error_message="No fields to update")

        if args['roll_number']:
            existing_student = Student.query.filter_by(roll_number=args['roll_number']).first()
            if existing_student and existing_student.student_id != student_id:
                abort(409, message="Student already exist")
            student.roll_number = args['roll_number']
        if args['first_name']:
            student.first_name = args['first_name']
        if args['last_name']:
            student.last_name = args['last_name']
            
        db.session.commit()
        return student, 200

    def delete(self, student_id):
        student = Student.query.get(student_id)
        if not student:
            abort(404, message="Student not found")
            
        Enrollment.query.filter_by(student_id=student_id).delete()
        
        db.session.delete(student)
        db.session.commit()
        return {"message": "Successfully Deleted"}, 200

class StudentListAPI(Resource):
    @marshal_with(student_fields)
    def post(self):
        args = student_post_parser.parse_args()

        if not args.get('roll_number'):
            return {"error_code": "STUDENT001", "error_message": "Roll Number required"}, 400
        if not args.get('first_name'):
            return {"error_code": "STUDENT002", "error_message": "First Name is required"}, 400

        if Student.query.filter_by(roll_number=args['roll_number']).first():
            abort(409, message="Student already exist")
            
        new_student = Student(
            roll_number=args['roll_number'],
            first_name=args['first_name'],
            last_name=args['last_name']
        )
        db.session.add(new_student)
        db.session.commit()
        return new_student, 201


# --- NEW: Enrollment API Resources ---

class EnrollmentAPI(Resource):
    
    @marshal_with(enrollment_fields)
    def get(self, student_id):
        # Check if student exists first
        student = Student.query.get(student_id)
        if not student:
            # Document specifies 400 for invalid student ID in this GET
            abort(400, message="Invalid Student Id") 
            
        enrollments = Enrollment.query.filter_by(student_id=student_id).all()
        if not enrollments:
            abort(404, message="Student is not enrolled in any course")
            
        return enrollments, 200

    @marshal_with(enrollment_fields)
    def post(self, student_id):
        # Check if student exists
        student = Student.query.get(student_id)
        if not student:
            # Doc specifies 404 for POST
            return {"error_code": "ENROLLMENT002", "error_message": "Student does not exist."}, 404
        
        args = enrollment_post_parser.parse_args()
        course_id = args['course_id']
        
        # Check if course exists
        course = Course.query.get(course_id)
        if not course:
            return {"error_code": "ENROLLMENT001", "error_message": "Course does not exist"}, 400

        # Check if enrollment already exists
        existing_enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
        if existing_enrollment:
            abort(409, message="Student is already enrolled in this course")

        new_enrollment = Enrollment(student_id=student_id, course_id=course_id)
        db.session.add(new_enrollment)
        db.session.commit()
        return new_enrollment, 201 # 201 Created

    def delete(self, student_id, course_id):
        # Check if student and course IDs are valid in the first place
        student = Student.query.get(student_id)
        course = Course.query.get(course_id)
        if not student or not course:
            abort(400, message="Invalid Student Id or Course Id.")

        # Find the specific enrollment
        enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
        if not enrollment:
            abort(404, message="Enrollment for the student not found")
            
        db.session.delete(enrollment)
        db.session.commit()
        return {"message": "Successfully deleted"}, 200


# --- Add Resources to API ---
api.add_resource(CourseListAPI, '/api/course')
api.add_resource(CourseAPI, '/api/course/<int:course_id>')

api.add_resource(StudentListAPI, '/api/student')
api.add_resource(StudentAPI, '/api/student/<int:student_id>')

# --- NEW: Add Enrollment Resources to API ---
api.add_resource(EnrollmentAPI, 
                 '/api/student/<int:student_id>/course', 
                 '/api/student/<int:student_id>/course/<int:course_id>')


# --- Main execution ---
if __name__ == "__main__":
    app.run(debug=True)