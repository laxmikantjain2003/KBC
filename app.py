# python backend (flask code)
# app.py
# pip install flask
# app.py
# pip install flask
from flask import Flask, render_template, request, redirect, session, jsonify, flash
import sqlite3
import os
import random
import json
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'kbc_secret'

# Ensure DB folder exists
if not os.path.exists('database'):
    os.makedirs('database')

# Initialize database
def init_db():
    try:
        with sqlite3.connect('database/kbc.db') as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT,
                    middle_name TEXT,
                    last_name TEXT,
                    age INTEGER,
                    email TEXT UNIQUE,
                    mobile TEXT,
                    password TEXT
                )
            ''')
            c.execute('''
                CREATE TABLE IF NOT EXISTS scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT,
                    score INTEGER,
                    date_played TEXT
                )
            ''')
            conn.commit()
    except Exception as e:
        print(f"Database initialization error: {e}")

init_db()

# Load questions from JSON with error handling
try:
    with open('questions.json','r') as f:
        questions = json.load(f)
except Exception as e:
    print(f"Error loading questions.json: {e}")
    questions = []

@app.route('/')
def home():
    return redirect('/splash')

@app.route('/splash')
def splash():
    return render_template('splash.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST':
        data = {key: request.form[key] for key in request.form}
        try:
            with sqlite3.connect('database/kbc.db') as conn:
                c = conn.cursor()
                c.execute("SELECT * FROM users WHERE email=?", (data['email'],))
                if c.fetchone():
                    message = "⚠️ Email already registered!"
                else:
                    hashed_password = generate_password_hash(data['password'])
                    c.execute("""INSERT INTO users 
                        (first_name, middle_name, last_name, age, email, mobile, password) 
                        VALUES (?, ?, ?, ?, ?, ?, ?)""",
                          (data['first_name'], data['middle_name'], data['last_name'], data['age'], data['email'], data['mobile'], hashed_password))
                    conn.commit()
                    return redirect('/login')
        except Exception as e:
            message = f"Error during registration: {e}"
    return render_template("register.html", message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            with sqlite3.connect('database/kbc.db') as conn:
                c = conn.cursor()
                c.execute("SELECT * FROM users WHERE email=?", (email,))
                user = c.fetchone()
            if user and check_password_hash(user[7], password):  # password field index
                session['user'] = email
                session['index'] = 0
                session['score'] = 0
                session['used_5050'] = False
                session['used_skip'] = False
                session['used_phone'] = False
                session['used_audience'] = False
                return redirect('/play')
            else:
                message = "❌ Incorrect email or password!"
        except Exception as e:
            message = f"Error during login: {e}"
    return render_template("login.html", message=message)

@app.route('/play', methods=['GET', 'POST'])
def play():
    if not questions:
        return "<h2>Questions data not available. Please contact admin.</h2>"
    if 'index' not in session:
        session['index'] = 0
    result = ""
    index = session['index']

    if request.method == 'POST':
        if 'answer' in request.form:
            selected = request.form['answer']
            correct = questions[index]['answer']
            if selected == correct:
                result = "✅ Correct!"
                session['score'] += 10
            else:
                result = f"❌ Wrong! Correct answer was {correct}."
            session['index'] += 1
        elif 'lifeline' in request.form:
            lifeline = request.form['lifeline']
            used_flag = None
            if lifeline == '5050':
                used_flag = session.get('used_5050')
            elif lifeline == 'skip':
                used_flag = session.get('used_skip')
            elif lifeline == 'phone':
                used_flag = session.get('used_phone')
            elif lifeline == 'audience':
                used_flag = session.get('used_audience')

            if used_flag:
                result = f"⚠️ You have already used the {lifeline} lifeline!"
            else:
                if lifeline == '5050':
                    session['used_5050'] = True
                elif lifeline == 'skip':
                    session['index'] += 1
                    session['used_skip'] = True
                elif lifeline == 'phone':
                    session['used_phone'] = True
                elif lifeline == 'audience':
                    session['used_audience'] = True

    if session['index'] >= len(questions):
        save_score(session['user'], session['score'])
        final_score = session['score']
        session.clear()
        return render_template("scorecard.html", score=final_score)

    q = questions[session['index']]
    options = q['options'].copy()

    if session.get('used_5050'):
        correct = q['answer']
        wrongs = [k for k in options.keys() if k != correct]
        removed = random.sample(wrongs, 2)
        for r in removed:
            del options[r]

    audience_poll = ""
    if session.get('used_audience'):
        audience_poll = f"🗳 Audience Poll Suggests: {q['answer']}"

    phone_hint = ""
    if session.get('used_phone'):
        phone_hint = f"📞 Your friend thinks it's: {q['answer']}"

    return render_template("play.html", question=q, options=options, result=result,
                           phone_hint=phone_hint, audience_poll=audience_poll,
                           used_5050=session.get('used_5050'),
                           used_skip=session.get('used_skip'),
                           used_phone=session.get('used_phone'),
                           used_audience=session.get('used_audience'))

def save_score(email, score):
    try:
        with sqlite3.connect('database/kbc.db') as conn:
            c = conn.cursor()
            c.execute("INSERT INTO scores (email, score, date_played) VALUES (?, ?, ?)",
                      (email, score, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
    except Exception as e:
        print(f"Error saving score: {e}")

@app.route('/leaderboard')
def leaderboard():
    top_scores = []
    try:
        with sqlite3.connect('database/kbc.db') as conn:
            c = conn.cursor()
            c.execute("SELECT email, score, date_played FROM scores ORDER BY score DESC, date_played DESC LIMIT 5")
            top_scores = c.fetchall()
    except Exception as e:
        print(f"Error fetching leaderboard: {e}")
    return render_template("leaderboard.html", top_scores=top_scores)

if __name__ == '__main__':
    # For development only, disable debug=True in production
    app.run(debug=True)



