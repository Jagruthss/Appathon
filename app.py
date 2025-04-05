from flask import Flask, request, render_template, redirect, url_for, jsonify, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Hardcoded credentials for demonstration purposes (username: 'admin', password: 'password123')
USER_CREDENTIALS = {
    "admin": "password123"
}

# Route for the login page
@app.route('/')
def login_page():
    return app.send_static_file('login.html')  # Serve the login page from static folder

# Route to handle login form submission
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Get the username and password from the frontend
    username = data.get('username')
    password = data.get('password')

    # Check if the credentials are correct
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        session['logged_in'] = True
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

# Route for the quiz page, accessible only after login
@app.route('/quiz')
def quiz_page():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))  # Redirect to login if not logged in
    return app.send_static_file('quiz.html')  # Serve the quiz page from static folder

# Route to handle quiz submission and calculate score
@app.route('/submit-quiz', methods=['POST'])
def submit_quiz():
    user_answers = request.get_json()
    score = 0

    # Questions and answers (hardcoded)
    questions = [
        {
            "question": "What is the capital of France?",
            "options": ["A) Berlin", "B) Madrid", "C) Paris", "D) Rome"],
            "correct": "C"
        },
        {
            "question": "Which planet is known as the Red Planet?",
            "options": ["A) Earth", "B) Mars", "C) Venus", "D) Jupiter"],
            "correct": "B"
        },
        {
            "question": "Who wrote 'To Kill a Mockingbird'?",
            "options": ["A) Harper Lee", "B) J.K. Rowling", "C) Ernest Hemingway", "D) Mark Twain"],
            "correct": "A"
        },
        {
            "question": "What is the largest ocean on Earth?",
            "options": ["A) Atlantic Ocean", "B) Arctic Ocean", "C) Indian Ocean", "D) Pacific Ocean"],
            "correct": "D"
        }
    ]

    # Calculate score based on answers
    for i, question in enumerate(questions):
        user_answer = user_answers.get(f'question{i}')
        if user_answer == question['correct']:
            score += 1

    return jsonify({"score": score})

if __name__ == "__main__":
    app.run(debug=True)
