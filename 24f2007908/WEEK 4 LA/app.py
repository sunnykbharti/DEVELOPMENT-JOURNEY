from flask.flask import Flask, render_template, request
import csv
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Ensure the static directory exists
if not os.path.exists('static'):
    os.makedirs('static')

def read_csv():
    """Reads the data from data.csv and returns it as a list of lists."""
    data = []
    try:
        with open('data.csv', 'r') as file:
            reader = csv.reader(file)
            # Skip header row
            next(reader)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print("Error: data.csv not found. Please make sure the file is in the same directory as app.py.")
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = read_csv()
        if not data:
            return render_template('error.html', message="Data file is empty or not found.")

        id_type = request.form.get('ID')
        id_value = request.form.get('id_value')

        if not id_value:
            return render_template('error.html', message="Wrong Inputs: ID value cannot be empty.")

        if id_type == 'student_id':
            student_data = []
            total_marks = 0
            student_exists = False
            for row in data:
                # row[0] is Student ID, row[2] is Marks
                if row[0] == id_value:
                    student_exists = True
                    student_data.append(row)
                    total_marks += int(row[2])
            
            if not student_exists:
                return render_template('error.html', message="Wrong Inputs: Student ID not found.")
                
            return render_template('student_details.html', student_data=student_data, total_marks=total_marks)

        elif id_type == 'course_id':
            course_marks = []
            course_exists = False
            for row in data:
                # row[1] is Course ID, row[2] is Marks
                if row[1] == id_value:
                    course_exists = True
                    course_marks.append(int(row[2]))

            if not course_exists:
                return render_template('error.html', message="Wrong Inputs: Course ID not found.")

            if not course_marks:
                 return render_template('error.html', message="No students are registered for this course.")


            avg_marks = sum(course_marks) / len(course_marks)
            max_marks = max(course_marks)

            # Generate and save histogram
            plt.figure()
            plt.hist(course_marks, bins=10, edgecolor='black')
            plt.title(f'Marks Distribution for Course {id_value}')
            plt.xlabel('Marks')
            plt.ylabel('Frequency')
            img_path = 'static/histogram.png'
            plt.savefig(img_path)
            plt.close()

            return render_template('course_details.html', avg_marks=f"{avg_marks:.2f}", max_marks=max_marks, img_path=img_path)
        
        else:
            return render_template('error.html', message="Wrong Inputs: Please select either Student ID or Course ID.")


    # This is for the GET request
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)