import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# --- App Configuration ---

# Get the absolute path of the directory containing this file
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# Configure the SQLite database, stored in the project directory
# Check if DATABASE_URL environment variable is set (for production on Render)
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Render's PostgreSQL URLs start with postgres://, but SQLAlchemy needs postgresql://
    database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    # Add this line to prevent a SQLAlchemy 1.4 warning
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping': True}
else:
    # Fallback to local sqlite database
    basedir = os.path.abspath(os.path.dirname(__file__))
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

        # Q3
        q3 = Question(text="What keyword is used to define a function in Python?", quiz=py_quiz)
        db.session.add(q3)
        o3_1 = Option(text="func", is_correct=False, question=q3)
        o3_2 = Option(text="def", is_correct=True, question=q3)
        o3_3 = Option(text="function", is_correct=False, question=q3)
        db.session.add_all([o3_1, o3_2, o3_3])

        # Q4
        q4 = Question(text="How do you create a single-line comment in Python?", quiz=py_quiz)
        db.session.add(q4)
        o4_1 = Option(text="// This is a comment", is_correct=False, question=q4)
        o4_2 = Option(text="/* This is a comment */", is_correct=False, question=q4)
        o4_3 = Option(text="# This is a comment", is_correct=True, question=q4)
        db.session.add_all([o4_1, o4_2, o4_3])

        # Q5
        q5 = Question(text="What is the correct way to create a dictionary?", quiz=py_quiz)
        db.session.add(q5)
        o5_1 = Option(text='my_dict = {"name": "John", "age": 30}', is_correct=True, question=q5)
        o5_2 = Option(text='my_dict = ["name", "John", "age", 30]', is_correct=False, question=q5)
        o5_3 = Option(text='my_dict = ("name": "John", "age": 30)', is_correct=False, question=q5)
        db.session.add_all([o5_1, o5_2, o5_3])

        # Q6
        q6 = Question(text="Which data type is immutable in Python?", quiz=py_quiz)
        db.session.add(q6)
        o6_1 = Option(text="list", is_correct=False, question=q6)
        o6_2 = Option(text="dict", is_correct=False, question=q6)
        o6_3 = Option(text="tuple", is_correct=True, question=q6)
        db.session.add_all([o6_1, o6_2, o6_3])

        # Q7
        q7 = Question(text="What does the len() function do?", quiz=py_quiz)
        db.session.add(q7)
        o7_1 = Option(text="Returns the length of an object", is_correct=True, question=q7)
        o7_2 = Option(text="Converts an object to a string", is_correct=False, question=q7)
        o7_3 = Option(text="Creates a new list", is_correct=False, question=q7)
        db.session.add_all([o7_1, o7_2, o7_3])

        # Q8
        q8 = Question(text="How do you check the data type of a variable 'x'?", quiz=py_quiz)
        db.session.add(q8)
        o8_1 = Option(text="type(x)", is_correct=True, question=q8)
        o8_2 = Option(text="datatype(x)", is_correct=False, question=q8)
        o8_3 = Option(text="x.type()", is_correct=False, question=q8)
        db.session.add_all([o8_1, o8_2, o8_3])

        # Q9
        q9 = Question(text="What operator is used for exponentiation (2 to the power of 3)?", quiz=py_quiz)
        db.session.add(q9)
        o9_1 = Option(text="^", is_correct=False, question=q9)
        o9_2 = Option(text="**", is_correct=True, question=q9)
        o9_3 = Option(text="pow", is_correct=False, question=q9)
        db.session.add_all([o9_1, o9_2, o9_3])

        # Q10
        q10 = Question(text="How do you start a 'for' loop to iterate over a list called 'my_list'?", quiz=py_quiz)
        db.session.add(q10)
        o10_1 = Option(text="for item in my_list:", is_correct=True, question=q10)
        o10_2 = Option(text="loop item in my_list:", is_correct=False, question=q10)
        o10_3 = Option(text="for my_list:", is_correct=False, question=q10)
        db.session.add_all([o10_1, o10_2, o10_3])

        # Create an "Entertainment" quiz
        ent_quiz = Quiz(title="Movie Trivia")
        db.session.add(ent_quiz)

        # Q1
        q11 = Question(text="What movie is this quote from: 'I'll be back'?", quiz=ent_quiz)
        db.session.add(q11)
        o11_1 = Option(text="Titanic", is_correct=False, question=q11)
        o11_2 = Option(text="The Terminator", is_correct=True, question=q11)
        o11_3 = Option(text="The Matrix", is_correct=False, question=q11)
        db.session.add_all([o11_1, o11_2, o11_3])

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
