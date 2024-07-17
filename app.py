#chat gpt가 작성

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 각 홀의 파 값과 사용한 클럽을 저장할 리스트
holes = []

# 템플릿에서 enumerate를 사용할 수 있도록 설정
@app.context_processor
def utility_processor():
    return dict(enumerate=enumerate)

@app.route('/')
def index():
    total_score = sum(hole['score'] for hole in holes)
    return render_template('index.html', holes=holes, total_score=total_score)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        par = int(request.form['par'])
        score = int(request.form['score'])
        clubs = request.form['clubs'].split(',')

        # 홀 기록 저장
        hole_record = {
            'par': par,
            'score': score,
            'clubs': clubs
        }
        holes.append(hole_record)
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/edit/<int:hole_id>', methods=['GET', 'POST'])
def edit(hole_id):
    if request.method == 'POST':
        par = int(request.form['par'])
        score = int(request.form['score'])
        clubs = request.form['clubs'].split(',')

        # 수정된 기록 저장
        holes[hole_id] = {
            'par': par,
            'score': score,
            'clubs': clubs
        }
        return redirect(url_for('index'))

    hole = holes[hole_id]
    return render_template('edit.html', hole=hole, hole_id=hole_id)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
