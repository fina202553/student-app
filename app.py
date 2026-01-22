from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from config import Config
from models import Database

# Initalize Flask application
app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    """ホームページ - すべての生徒を表示"""
    students = Database.get_all_students()
    return render_template('index.html', students=students)

@app.route('/add_student', methods=['POST'])
def add_student():
    """新しい学生のフォーム送信を処理します"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        student_number = request.form.get('student_number', '').strip()

        # Validate input
        if not name or not student_number:
            flash('× すべてのフィールドを入力してください', 'error')
            return redirect(url_for('index'))

        if len(name) > 100:
            flash('× 名前が長すぎます（最大100文字）', 'error')
            return redirect(url_for('index'))

        if len(student_number) > 20:
            flash('× 学生番号が長すぎます（最大20文字）', 'error')
            return redirect(url_for('index'))

        # Add student to database
        success, message = Database.add_student(name, student_number)
        
        if success:
            flash(f'✔ {message}', 'success')
        else:
            flash(f'× {message}', 'error')

        return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search_students():
    """名前または学生番号で学生を検索します"""
    query = request.args.get('query', '').strip()
    if query:
        students = Database.search_students(query)
    else:
        students = Database.get_all_students()
        
    return render_template('index.html', students=students, search_query=query)

@app.route('/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    """IDで学生を削除します"""
    if Database.delete_student(student_id):
        flash('✔ 学生が正常に削除されました！', 'success')
    else:
        flash('× 学生削除エラー', 'error')
        
    return redirect(url_for('index'))

@app.route('/api/students', methods=['GET'])
def api_students():
    """APIエンドポイント - すべての学生を取得します（将来の使用のため）"""
    students = Database.get_all_students()
    students_list = []
    for student in students:
        students_list.append({
            'id': student[0],
            'name': student[1],
            'student_number': student[2],
            'created_at': student[3].isoformat()
        })
    return jsonify(students_list)

@app.errorhandler(404)
def not_found_error(error):
    """404エラーを処理します"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """500エラーを処理します"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Initialize database tables
    print("● 学生記録アプリケーションを起動しています…")
    Database.init_db()

    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)