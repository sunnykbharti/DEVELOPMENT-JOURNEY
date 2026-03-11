from app import db,Course,app
with app.app_context():
    courses=[
        Course(course_id=1, course_code="CSE01", course_name="MAD I", course_descriptions="MAD1"),
        Course(course_id=2, course_code="CSE02", course_name="MAD II", course_descriptions="MAD12"),
        Course(course_id=3, course_code="CSE03", course_name="MAD II", course_descriptions="MAD123"),
        Course(course_id=4, course_code="CSE01", course_name="MAD III", course_descriptions="MAD1234")
    ]

db.session.add_all(courses)
db.session.commit()