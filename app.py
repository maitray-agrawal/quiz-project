import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# --- App Configuration ---

# Get the absolute path of the directory containing this file
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# Configure the SQLite database, stored in the project directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'quiz.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# --- Database Models ---

# Model for a Quiz
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    # Relationship: A quiz can have many questions
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Quiz {self.title}>'

# Model for a Question
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    # Foreign Key: Links this question to a specific quiz
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    # Relationship: A question can have many options
    options = db.relationship('Option', backref='question', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Question {self.text}>'

# Model for an Option
class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False, default=False)
    # Foreign Key: Links this option to a specific question
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

    def __repr__(self):
        return f'<Option {self.text}>'

# --- Database Initialization ---

@app.cli.command('init-db')
def init_db_command():
    """Creates the database tables and populates with sample data."""
    with app.app_context():
        db.drop_all()  # Clear existing data
        db.create_all()  # Create new tables

        # Create a "Python Basics" quiz
        py_quiz = Quiz(title="Python Basics")
        db.session.add(py_quiz)

        # Q1
        q1 = Question(text="What does 'print()' do in Python?", quiz=py_quiz)
        db.session.add(q1)
        o1_1 = Option(text="Prints text to the console", is_correct=True, question=q1)
        o1_2 = Option(text="Saves a file", is_correct=False, question=q1)
        o1_3 = Option(text="Runs a web server", is_correct=False, question=q1)
        db.session.add_all([o1_1, o1_2, o1_3])

        # Q2
        q2 = Question(text="What is a 'list' in Python?", quiz=py_quiz)
        db.session.add(q2)
        o2_1 = Option(text="A single number", is_correct=False, question=q2)
        o2_2 = Option(text="A collection of items", is_correct=True, question=q2)
        o2_3 = Option(text="A type of loop", is_correct=False, question=q2)
        db.session.add_all([o2_1, o2_2, o2_3])

        # Create an "Entertainment" quiz
        ent_quiz = Quiz(title="Movie Trivia")
        db.session.add(ent_quiz)

        # Q1
        q3 = Question(text="What movie is this quote from: 'I'll be back'?", quiz=ent_quiz)
        db.session.add(q3)
        o3_1 = Option(text="Titanic", is_correct=False, question=q3)
        o3_2 = Option(text="The Terminator", is_correct=True, question=q3)
        o3_3 = Option(text="The Matrix", is_correct=False, question=q3)
        db.session.add_all([o3_1, o3_2, o3_3])

        # Commit all changes to the database
        db.session.commit()
        print('Initialized the database with sample data.')

# --- Web Routes ---

@app.route('/')
def index():
    """Home page: Displays a list of all available quizzes."""
    quizzes = Quiz.query.all()
    return render_template('index.html', quizzes=quizzes)

@app.route('/quiz/<int:quiz_id>')
def quiz(quiz_id):
    """Quiz page: Displays all questions for the selected quiz."""
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('quiz.html', quiz=quiz)

@app.route('/submit/<int:quiz_id>', methods=['POST'])
def submit(quiz_id):
    """Processes the quiz submission."""
    quiz = Quiz.query.get_or_404(quiz_id)
    score = 0
    total = len(quiz.questions)

    # Loop through each question in the quiz
    for question in quiz.questions:
        # 'request.form' gets the data submitted from the HTML form
        # We named our radio buttons 'question_X' where X is the question.id
        submitted_option_id = request.form.get(f'question_{question.id}')

        if submitted_option_id:
            # Find the option the user selected
            selected_option = Option.query.get(submitted_option_id)
            # Check if the selected option is the correct one
            if selected_option and selected_option.is_correct:
                score += 1

    # Redirect to the results page, passing the score and total
    return redirect(url_for('results', score=score, total=total))

@app.route('/results/<int:score>/<int:total>')
def results(score, total):
    """Results page: Displays the user's final score."""
    return render_template('results.html', score=score, total=total)

# --- Run the Application ---

if __name__ == '__main__':
    with app.app_context():
        # This will create the db file if it doesn't exist,
        # but won't overwrite or init data.
        db.create_all() 
    app.run(debug=True)
