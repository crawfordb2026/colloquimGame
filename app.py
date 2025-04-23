# app.py
from flask import Flask, render_template, request, redirect, url_for, session
import random
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a better secret key in production

questions = [
    {"question": "What is 5 + 7?", "answer": "12"},
    {"question": "What comes next? 2, 4, 6, ?", "answer": "8"},
    {"question": "What is 9 - 3?", "answer": "6"},
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "What is 3 * 3?", "answer": "9"}
]

@app.route('/')
def home():
    session['start_time'] = time.time()
    session['score'] = 0
    session['index'] = 0
    return redirect(url_for('game'))

@app.route('/game', methods=['GET', 'POST'])
def game():
    index = session.get('index', 0)
    score = session.get('score', 0)

    if index >= len(questions):
        return redirect(url_for('result'))

    question = questions[index]

    if request.method == 'POST':
        user_answer = request.form.get('answer').strip().lower()
        correct_answer = question['answer'].strip().lower()

        if user_answer == correct_answer:
            session['score'] += 1
        session['index'] += 1
        return redirect(url_for('game'))

    return render_template('game.html', question=question['question'], index=index + 1)

@app.route('/result')
def result():
    end_time = time.time()
    total_time = round(end_time - session.get('start_time', end_time), 2)
    return render_template('result.html', score=session.get('score', 0), total_time=total_time)

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


