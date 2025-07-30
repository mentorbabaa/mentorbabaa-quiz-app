from flask import Flask, render_template, request, redirect, session, jsonify
import os
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# Load the correct .env file based on APP_ENV
env = os.getenv("APP_ENV", "local")
env_file = f".env.{env}"
print(f"🔧 Loading config from {env_file}")
load_dotenv(env_file)

USE_SQLITE = os.getenv("USE_SQLITE", "true").lower() == "true"

app = Flask(__name__)
app.secret_key = 'mentorbaba_secret'

# Initialize database connection
if USE_SQLITE:
    import sqlite3
    DB_PATH = os.getenv("SQLITE_DB_PATH", "app.db")
    db = sqlite3.connect(DB_PATH, check_same_thread=False)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    print(f"✅ Using SQLite at {DB_PATH}")
else:
    import mysql.connector
    db = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )
    cursor = db.cursor(dictionary=True)
    print(f"✅ Connected to MySQL at {os.getenv('MYSQL_HOST')}")

# ---------- Routes ---------- #

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    if USE_SQLITE:
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    else:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))

    user = cursor.fetchone()
    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['id']
        return redirect('/confirm')
    return "Invalid credentials"

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = generate_password_hash(request.form['password'])

    try:
        if USE_SQLITE:
            cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        else:
            cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        db.commit()
    except:
        return "User already exists"

    return redirect('/')

@app.route('/confirm')
def confirm():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('confirm.html')

@app.route('/start')
def start_quiz():
    if 'user_id' not in session:
        return redirect('/')
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    return render_template('quiz.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    if 'user_id' not in session:
        return redirect('/')
    score = 0
    data = request.get_json()

    for qid, ans in data.items():
        if USE_SQLITE:
            cursor.execute("SELECT correct_answer FROM questions WHERE id = ?", (qid,))
        else:
            cursor.execute("SELECT correct_answer FROM questions WHERE id = %s", (qid,))
        correct = cursor.fetchone()
        is_correct = correct['correct_answer'] == ans
        if is_correct:
            score += 1
        if USE_SQLITE:
            cursor.execute(
                "INSERT INTO answers (user_id, question_id, selected_answer, is_correct) VALUES (?, ?, ?, ?)",
                (session['user_id'], qid, ans, is_correct)
            )
        else:
            cursor.execute(
                "INSERT INTO answers (user_id, question_id, selected_answer, is_correct) VALUES (%s, %s, %s, %s)",
                (session['user_id'], qid, ans, is_correct)
            )
    db.commit()
    return jsonify({'score': score})

@app.route('/result')
def result():
    if 'user_id' not in session:
        return redirect('/')
    if USE_SQLITE:
        cursor.execute("SELECT COUNT(*) as total, SUM(is_correct) as correct FROM answers WHERE user_id = ?", (session['user_id'],))
    else:
        cursor.execute("SELECT COUNT(*) as total, SUM(is_correct) as correct FROM answers WHERE user_id = %s", (session['user_id'],))
    res = cursor.fetchone()
    correct = res['correct'] if res['correct'] is not None else 0
    incorrect = res['total'] - correct
    return render_template('result.html', correct=correct, incorrect=incorrect, total=res['total'])

if __name__ == '__main__':
    app.run(debug=True)
