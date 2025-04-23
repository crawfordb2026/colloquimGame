from flask import Flask, render_template, request, redirect, url_for, session
import random
import time
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key in production

# Sample questions
questions = [
    {"question": "What is the derivative of sin(x)?", "answer": "cos(x)"},
    {"question": "What is the antiderivative of 2x?", "answer": "x^2"},
    {"question": "What is (5^2 - 3^2)?", "answer": "16"},
    {"question": "What is the derivative of x^2 + 3x?", "answer": "2x + 3"},
    {"question": "What is the value of cos(0)?", "answer": "1"},
    {"question": "What is 5 factorial (5!)?", "answer": "120"},
    {"question": "Solve for x: 2x + 3 = 9", "answer": "3"},
    {"question": "What is 2^4?", "answer": "16"},
    {"question": "What’s the square root of 81?", "answer": "9"},
    {"question": "What’s the integral of sec^2(x)?", "answer": "tan(x)"}
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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
