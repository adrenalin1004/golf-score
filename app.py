from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

golf_courses = {}

@app.context_processor
def utility_processor():
    return dict(enumerate=enumerate)

@app.route('/')
def index():
    return render_template('index.html', golf_courses=golf_courses)

@app.route('/course/<course_name>/<date>')
def view_course(course_name, date):
    if course_name in golf_courses and date in golf_courses[course_name]:
        holes = golf_courses[course_name][date]
        total_score = sum(hole['score'] for hole in holes)
        return render_template('view_course.html', holes=holes, total_score=total_score, course_name=course_name, date=date)
    return "No records found for this course and date.", 404

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        course_name = request.form['course_name']
        date = request.form['date']

        if course_name not in golf_courses:
            golf_courses[course_name] = {}

        if date not in golf_courses[course_name]:
            golf_courses[course_name][date] = [{'par': 0, 'score': 0, 'clubs': []} for _ in range(18)]

        return redirect(url_for('view_course', course_name=course_name, date=date))

    return render_template('add.html')

@app.route('/record/<course_name>/<date>/<int:hole_id>', methods=['GET', 'POST'])
def record(course_name, date, hole_id):
    if request.method == 'POST':
        par = int(request.form['par'])
        score = int(request.form['score'])
        clubs = request.form['clubs'].split(',')

        golf_courses[course_name][date][hole_id] = {
            'par': par,
            'score': score,
            'clubs': clubs
        }
        return redirect(url_for('view_course', course_name=course_name, date=date))

    hole = golf_courses[course_name][date][hole_id]
    return render_template('record.html', hole=hole, hole_id=hole_id, course_name=course_name, date=date)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
