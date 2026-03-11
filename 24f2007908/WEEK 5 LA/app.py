from flask import Flask, request, redirect
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Student(db.Model):
    student_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    roll_number=db.Column(db.String(200),nullable=False,unique=True)
    first_name=db.Column(db.String(200),nullable=False)
    last_name=db.Column(db.String(200))

class Course(db.Model):
    courses={'course_1':1,'course_2':2,'course_3':3,'course_4':4}
    #course_names = {1: 'MAD I', 2: 'DBMS', 3: 'PDSA', 4: 'BDM'}
    course_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    course_code=db.Column(db.String(200),nullable=False,unique=True)
    course_name=db.Column(db.String(200),nullable=False)
    course_description=db.Column(db.String(800))

class Enrollments(db.Model):
    enrollment_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    estudent_id=db.Column(db.Integer,db.ForeignKey('Student.student_id'),nullable=False)
    ecourse_id=db.Column(db.Integer,db.ForeignKey('Course.course_id'),nullable=False)

# # with app.app_context():
#     db.create_all()

#     if Course.query.count() == 0:
#         # Create course objects
#         mad_i = Course(course_id=1, course_code='C1', course_name='MAD I', course_description='MODERN APPLICATION DEVELOPMENT I')
#         dbms = Course(course_id=2, course_code='C2', course_name='DBMS', course_description='MODERN APPLICATION DEVELOPMENT I')
#         pdsa = Course(course_id=3, course_code='C3', course_name='PDSA', course_description='MODERN APPLICATION DEVELOPMENT I')
#         bdm = Course(course_id=4, course_code='C4', course_name='BDM', course_description='MODERN APPLICATION DEVELOPMENT I')
        
#         # Add all courses to the session
#         db.session.add_all([mad_i, dbms, pdsa, bdm])
#         # Commit the changes to the database
#         db.session.commit()
#     # --- End of FIX ---

app.app_context().push()

@app.route('/',methods=['GET','POST'])
def home():
    students=Student.query.all()
    return render_template('home.html',students=students )

@app.route('/student/create',methods=['GET','POST'])
def add():
    if request.method=='GET':
        return render_template('add_students.html')
    elif request.method=='POST':
        roll=request.form.get('roll')
        f_name=request.form.get('f_name')
        l_name=request.form.get('l_name')
        course=request.form.getlist('courses')
        exist=Student.query.filter_by(roll_number=roll).first()
        if exist is None:
            db.session.add(Student(roll_number=roll,first_name=f_name,last_name=l_name))
            db.session.commit()
            courses=request.form.getlist('courses')
            for course in courses:
                course_id = Course.courses[course_value]
                db.session.add(Enrollments(estudent_id=new_student.student_id, ecourse_id=course_id))
                db.session.commit()
            return  redirect('/')
        return render_template('exists.html')
    
@app.route('/student/<int:student_id>/update',methods=['GET','POST'])
def update(student_id):
    if request.method=='GET':
        row=Student.query.filter_by(student_id=student_id).first()
        enrolls=Enrollments.query.filter_by(estudent_id=student_id).all()
        cid=[enroll.ecourse_id for enroll in enrolls]
        return render_template("update.html",row=row,cid=cid)
    
    elif request.method=='POST':
        stud=Student.query.filter_by(student_id=student_id).first()
        stud.first_name=request.form['f_name']
        stud.last_name=request.form['l_name']
        Enrollments.query.filter_by(estudent_id=student_id).delete()
        for course in request.form.getlist('courses'):
            db.session.add(Enrollments(estudent_id=student_id,ecourse_id=Course.courses[course]))
        db.session.commit()
        return redirect('/')

# @app.route('/student/<int:student_id>')
# def student_details(student_id):
#     student = Student.query.get(student_id)
#     enrolls = Enrollments.query.filter_by(estudent_id=student_id).all()
    
#     # Get course names from the IDs
#     enrolled_courses = []
#     for enroll in enrolls:
#         if enroll.ecourse_id in Course.course_names:
#             enrolled_courses.append(Course.course_names[enroll.ecourse_id])
            
#     return render_template("student_details.html", student=student, courses=enrolled_courses)

@app.route('/student/<int:student_id>/delete',methods=['GET'])
def delete(student_id):
    Enrollments.query.filter_by(estudent_id=student_id).delete()
    Student.query.filter_by(student_id=student_id).delete()
    db.session.commit()
    return redirect('/')

@app.route('/student/<int:student_id>',methods=['GET','POST'])
def view(student_id):
    details_s=Student.query.filter_by(student_id=student_id).first()
    enrollment=Enrollments.query.filter_by(estudent_id=student_id).all()
    courses=[]
    for enroll in enrollment:
        course=Course.query.filter_by(course=Enrollments.ecourse_id)
        if course:
            courses.append(course)
        return render_template('view.html',student=details_s,courses=course)



if __name__=="__main__":
    app.run(debug=True)