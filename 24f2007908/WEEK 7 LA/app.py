from flask import Flask, render_template, request, redirect, url_for, abort, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

# --- Setup ---
app = Flask(__name__)
# Database URI must be 'sqlite:///week7_database.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///week7_database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Models ---
# Table 1: student
class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)

    # Relationship to enrollments (cascades delete)
    enrollments = db.relationship('Enrollment', backref='student', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"Student(ID={self.student_id}, Roll={self.roll_number})"

# Table 2: course
class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)

    # Relationship to enrollments (cascades delete)
    enrollments = db.relationship('Enrollment', backref='course', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"Course(ID={self.course_id}, Code={self.course_code})"

# Table 3: enrollments (Association Table)
class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # estudent_id must be Foreign Key to student.student_id, Not Null
    estudent_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    # ecourse_id must be Foreign Key to course.course_id, Not Null
    ecourse_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)

    def __repr__(self):
        return f"Enrollment(ID={self.enrollment_id}, Student={self.estudent_id}, Course={self.ecourse_id})"


# --- Custom Response Class to enforce 200 status on success ---
class CustomResponse(Response):
    @classmethod
    def force_type(cls, rv, environ=None):
        # Override to set the status code to 200 if not explicitly set and not a redirect
        if isinstance(rv, str) and not rv.startswith('<!DOCTYPE'):
            # Only for template rendering/text responses, not redirects
            rv = (rv, 200)
        return super().force_type(rv, environ)

app.response_class = CustomResponse

# Helper for rendering error page
def render_error(message, back_uri):
    return render_template('error.html', message=message, back_uri=back_uri)

# --- Student CRUD Operations ---

@app.route('/')
def students_list():
    """1. Home page: Displays all students."""
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/student/create', methods=['GET', 'POST'])
def create_student():
    """2. Student creation: GET for form, POST for submission."""
    if request.method == 'GET':
        return render_template('create_student.html')
    
    if request.method == 'POST':
        roll = request.form.get('roll')
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')

        if not roll or not f_name:
            # Should not happen if 'required' is used, but good practice
            return render_error("Missing required fields.", url_for('students_list'))

        try:
            new_student = Student(roll_number=roll, first_name=f_name, last_name=l_name)
            db.session.add(new_student)
            db.session.commit()
            return redirect(url_for('students_list'))
        except exc.IntegrityError:
            db.session.rollback()
            # If roll number already exists (Unique constraint violation)
            message = "Student already exists. Please use different Roll Number !!"
            return render_error(message, url_for('students_list'))

@app.route('/student/<int:student_id>/update', methods=['GET', 'POST'])
def update_student(student_id):
    """3. Student update: GET for form, POST for submission and enrollment."""
    student = Student.query.get(student_id)
    if not student:
        abort(404) # Not found

    courses = Course.query.all()

    if request.method == 'GET':
        return render_template('update_student.html', student=student, courses=courses)
    
    if request.method == 'POST':
        # 1. Update personal details
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')
        course_id_to_enroll = request.form.get('course')

        if not f_name:
            return render_error("First Name is required.", url_for('students_list'))

        student.first_name = f_name
        student.last_name = l_name

        # 2. Handle course enrollment
        if course_id_to_enroll:
            course_id = int(course_id_to_enroll)
            # Check if student is already enrolled in this course
            existing_enrollment = Enrollment.query.filter_by(
                estudent_id=student_id, ecourse_id=course_id
            ).first()

            if not existing_enrollment:
                # Create new enrollment if it doesn't exist
                new_enrollment = Enrollment(estudent_id=student_id, ecourse_id=course_id)
                db.session.add(new_enrollment)
        
        try:
            db.session.commit()
            return redirect(url_for('students_list'))
        except Exception:
            db.session.rollback()
            return render_error("An error occurred during update or enrollment.", url_for('students_list'))


@app.route('/student/<int:student_id>/delete')
def delete_student(student_id):
    """4. Student deletion: Deletes student and all associated enrollments."""
    student = Student.query.get(student_id)
    if not student:
        # If student doesn't exist, we just redirect back to be safe/simple
        return redirect(url_for('students_list'))
    
    try:
        # Thanks to cascade='all, delete-orphan' in Student model, enrollments will be deleted too.
        db.session.delete(student)
        db.session.commit()
        return redirect(url_for('students_list'))
    except Exception:
        db.session.rollback()
        return render_error("Could not delete student.", url_for('students_list'))


@app.route('/student/<int:student_id>')
def student_details(student_id):
    """5. Student details page."""
    student = Student.query.get(student_id)
    if not student:
        abort(404) # Not found
    
    # Eagerly load course details for enrollments
    enrollments = db.session.query(Enrollment, Course).join(Course).filter(
        Enrollment.estudent_id == student_id
    ).all()

    return render_template('student_details.html', student=student, enrollments=enrollments)

@app.route('/student/<int:student_id>/withdraw/<int:course_id>')
def withdraw_course(student_id, course_id):
    """6. Withdraw from a course (delete enrollment)."""
    enrollment = Enrollment.query.filter_by(
        estudent_id=student_id, ecourse_id=course_id
    ).first()

    if enrollment:
        try:
            db.session.delete(enrollment)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return render_error("Could not withdraw student from course.", url_for('students_list'))
    
    # Redirect to home page as requested in prompt (point 6)
    return redirect(url_for('students_list'))

# --- Course CRUD Operations ---

@app.route('/courses')
def courses_list():
    """7. Courses page: Displays all courses."""
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)

@app.route('/course/create', methods=['GET', 'POST'])
def create_course():
    """8. Course creation: GET for form, POST for submission."""
    if request.method == 'GET':
        return render_template('create_course.html')
    
    if request.method == 'POST':
        code = request.form.get('code')
        c_name = request.form.get('c_name')
        desc = request.form.get('desc')

        if not code or not c_name:
            return render_error("Missing required fields.", url_for('courses_list'))

        try:
            new_course = Course(course_code=code, course_name=c_name, course_description=desc)
            db.session.add(new_course)
            db.session.commit()
            return redirect(url_for('courses_list'))
        except exc.IntegrityError:
            db.session.rollback()
            # If course code already exists (Unique constraint violation)
            message = "Course already exists. Please create a different course !!"
            return render_error(message, url_for('courses_list'))

@app.route('/course/<int:course_id>/update', methods=['GET', 'POST'])
def update_course(course_id):
    """9. Course update: GET for form, POST for submission."""
    course = Course.query.get(course_id)
    if not course:
        abort(404)
    
    if request.method == 'GET':
        return render_template('update_course.html', course=course)
    
    if request.method == 'POST':
        c_name = request.form.get('c_name')
        desc = request.form.get('desc')

        if not c_name:
            return render_error("Course Name is required.", url_for('courses_list'))

        course.course_name = c_name
        course.course_description = desc
        
        try:
            db.session.commit()
            return redirect(url_for('courses_list'))
        except Exception:
            db.session.rollback()
            return render_error("An error occurred during course update.", url_for('courses_list'))

@app.route('/course/<int:course_id>/delete')
def delete_course(course_id):
    """10. Course deletion: Deletes course and all associated enrollments."""
    course = Course.query.get(course_id)
    if not course:
        # Redirect to home page as requested
        return redirect(url_for('students_list'))
    
    try:
        # Thanks to cascade='all, delete-orphan' in Course model, enrollments will be deleted too.
        db.session.delete(course)
        db.session.commit()
        # Redirect to home page (students list) as requested in prompt (point 10)
        return redirect(url_for('students_list'))
    except Exception:
        db.session.rollback()
        return render_error("Could not delete course.", url_for('students_list'))


@app.route('/course/<int:course_id>')
def course_details(course_id):
    """11. Course details page."""
    course = Course.query.get(course_id)
    if not course:
        abort(404)
    
    # Eagerly load student details for enrollments
    enrollments = db.session.query(Enrollment, Student).join(Student).filter(
        Enrollment.ecourse_id == course_id
    ).all()
    
    return render_template('course_details.html', course=course, enrollments=enrollments)

@app.route('/error/<message>/<back_uri>')
def custom_error_page(message, back_uri):
    """Helper route to display a custom error page."""
    return render_template('error.html', message=message, back_uri=back_uri)


if __name__ == '__main__':
    # NOTE: db.create_all() is omitted as per instructions.
    # A manual schema setup or an external setup step is assumed.
    # To run, you would normally run this file and ensure the 'week7_database.sqlite3' file is created 
    # with the correct schema defined above.
    app.run(debug=True)