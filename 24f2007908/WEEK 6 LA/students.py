from app import app, db, Student, Course, Enrollment

def init_db():
    with app.app_context():
        # 1. Create the tables based on the Models defined in app.py
        db.create_all()
        print("Database tables created successfully!")

        # 2. Check if data exists, if not, add some dummy data for testing
        if not Student.query.first():
            print("Populating database with sample data...")
            
            # Create a Student
            student1 = Student(
                roll_number="CS202401", 
                first_name="Sunny", 
                last_name="Bharti"
            )
            
            # Create a Course
            course1 = Course(
                course_name="Data Structures and Algorithms", 
                course_code="CS101", 
                course_description="Intro to DSA with Python"
            )

            # Add to session
            db.session.add(student1)
            db.session.add(course1)
            db.session.commit() # Commit to get IDs generated

            # Create an Enrollment (Link them)
            # We use the IDs that were just generated
            enrollment1 = Enrollment(
                student_id=student1.student_id, 
                course_id=course1.course_id
            )
            
            db.session.add(enrollment1)
            db.session.commit()
            
            print("Sample data added: 1 Student, 1 Course, 1 Enrollment.")
        else:
            print("Database already contains data.")

if __name__ == "__main__":
    init_db()