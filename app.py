import os
import logging
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from quiz_parser import list_quiz_files, parse_quiz_file

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "quiz_app_secret_key")

# Create quizzes directory if it doesn't exist
quizzes_dir = os.path.join(os.getcwd(), "quizzes")
if not os.path.exists(quizzes_dir):
    os.makedirs(quizzes_dir)

@app.route('/')
def index():
    """Display the list of available quizzes."""
    quizzes = list_quiz_files(quizzes_dir)
    return render_template('index.html', quizzes=quizzes)

@app.route('/quiz/<quiz_name>')
def quiz(quiz_name):
    """Load and display a quiz."""
    quiz_path = os.path.join(quizzes_dir, quiz_name)
    
    try:
        quiz_data = parse_quiz_file(quiz_path)
        session['current_quiz'] = quiz_data
        session['quiz_name'] = quiz_name
        session['current_question'] = 0
        session['answers'] = []
        
        return render_template('quiz.html', 
                              quiz_name=quiz_name,
                              quiz_data=quiz_data,
                              current_question=0)
    except Exception as e:
        logging.error(f"Error loading quiz {quiz_name}: {str(e)}")
        return render_template('index.html', 
                              quizzes=list_quiz_files(quizzes_dir),
                              error=f"Error loading quiz: {str(e)}")

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    """Process submitted answer and move to next question or results."""
    if 'current_quiz' not in session:
        return redirect(url_for('index'))
    
    quiz_data = session['current_quiz']
    current_question = session['current_question']
    
    # Get the selected answer
    answer = request.form.get('answer')
    
    # Store the answer
    answers = session.get('answers', [])
    answers.append(answer)
    session['answers'] = answers
    
    # Move to the next question
    current_question += 1
    session['current_question'] = current_question
    
    # If all questions have been answered, go to results
    if current_question >= len(quiz_data['questions']):
        return redirect(url_for('results'))
    
    # Otherwise, go to the next question
    return render_template('quiz.html',
                          quiz_name=session['quiz_name'],
                          quiz_data=quiz_data,
                          current_question=current_question)

@app.route('/results')
def results():
    """Display quiz results."""
    if 'current_quiz' not in session or 'answers' not in session:
        return redirect(url_for('index'))
    
    quiz_data = session['current_quiz']
    answers = session['answers']
    quiz_name = session['quiz_name']
    
    # Calculate the score
    correct_count = 0
    results = []
    
    for i, question in enumerate(quiz_data['questions']):
        user_answer = answers[i] if i < len(answers) else None
        correct_answer = question['correct_answer']
        is_correct = user_answer == correct_answer
        
        if is_correct:
            correct_count += 1
        
        results.append({
            'question': question['question'],
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': is_correct,
            'options': question['options']
        })
    
    score_percentage = (correct_count / len(quiz_data['questions'])) * 100
    
    return render_template('results.html',
                          quiz_name=quiz_name,
                          results=results,
                          score=correct_count,
                          total=len(quiz_data['questions']),
                          percentage=score_percentage)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
