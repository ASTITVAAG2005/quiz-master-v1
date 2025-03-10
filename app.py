import os , json 
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Text  


# Initializing Flask app
app = Flask(__name__)
app.secret_key = "astitva"

# Database configuration
current_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(current_dir, 'mydatabase.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static'

# Initializing the database
db = SQLAlchemy(app)

# predefined admin details 
def create_admin():
    with app.app_context():
        admin = User.query.filter_by(Role="admin").first()
        if not admin:
            new_admin = User(
                Username="admin",
                Email="admin@example.com",
                Password="admin123",  # Keeping plaintext as per your requirement
                Fullname="Admin User",
                Qualification="System Admin",
                DOB=datetime.strptime("2000-01-01", "%Y-%m-%d").date(),  # Convert string to date object
                Role="admin"
            )
            db.session.add(new_admin)
            db.session.commit()
        


# -------------------------------- Models and Tables ---------------------------------------- #

class User(db.Model):
    __tablename__ = 'user'
    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.String(500), nullable=False, unique=True)
    Email = db.Column(db.String(500), nullable=False, unique=True)
    Password = db.Column(db.String(500), nullable=False)
    Fullname = db.Column(db.String(500), nullable=False)
    Qualification = db.Column(db.String(500), nullable=False)
    DOB = db.Column(db.Date, nullable=False)
    Role = db.Column(db.String(10), nullable=False, default="user")  # 'admin' or 'user'

class Subject(db.Model):
    __tablename__ = 'subject'
    SubjectID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Subjectname = db.Column(db.String(500), nullable=False)
    Description = db.Column(db.String(500), nullable=False)

class Chapter(db.Model):
    __tablename__ = 'chapter'
    ChapterID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Chaptername = db.Column(db.String(500), nullable=False)
    Description = db.Column(db.String(500), nullable=False)

    QuizR = db.relationship('Quiz', backref='chapter', lazy=True)
    SubjectID = db.Column(db.Integer, db.ForeignKey('subject.SubjectID'), nullable=False)
    subject = db.relationship('Subject', backref='chapters')  


class Quiz(db.Model):
    __tablename__ = 'quiz'
    QuizID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Date_of_quiz = db.Column(db.Date, nullable=False)
    Time_duration = db.Column(db.String(5), nullable=False)  # Stores "HH:MM"
    Remarks = db.Column(db.String(500))
    ChapterID = db.Column(db.Integer, db.ForeignKey('chapter.ChapterID'), nullable=False)
    QuestionsR = db.relationship('Questions', backref='quiz', lazy=True)

class Questions(db.Model):
    __tablename__ = 'questions'
    QuestionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Question_statement = db.Column(db.String(500), nullable=False)
    Option1 = db.Column(db.String(500), nullable=False)
    Option2 = db.Column(db.String(500), nullable=False)
    Option3 = db.Column(db.String(500), nullable=False)
    Option4 = db.Column(db.String(500), nullable=False)
    Correct_option = db.Column(db.String(500), nullable=False)
    QuizID = db.Column(db.Integer, db.ForeignKey('quiz.QuizID'), nullable=False)

class UserAnswers(db.Model):
    __tablename__ = 'user_answers'
    AnswerID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ScoreID = db.Column(db.Integer, db.ForeignKey('score.ScoreID'), nullable=False)  # Links to Score table
    QuestionID = db.Column(db.Integer, db.ForeignKey('questions.QuestionID'), nullable=False)  # Links to Questions table
    SelectedAnswer = db.Column(db.String(500), nullable=True)  # Stores the user's selected answer

    # Relationships
    score = db.relationship('Score', backref='user_answers')
    question = db.relationship('Questions', backref='user_answers')


class Score(db.Model):
    __tablename__ = 'score'
    ScoreID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    QuizID = db.Column(db.Integer, db.ForeignKey('quiz.QuizID'), nullable=False)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'), nullable=False)
    TimeStamp = db.Column(db.DateTime, default=db.func.current_timestamp())  # Auto-fills time of attempt
    TotalScore = db.Column(db.Float, nullable=False)

    user = db.relationship('User', backref='scores')
    quiz = db.relationship('Quiz', backref='scores')


# -------------------------------- admin authentication ----------------------------------- #




@app.route('/adminlogin', methods=['POST'])
def adminlogin():
    username = request.form['username']
    password = request.form['password']
    admin = User.query.filter_by(Username=username, Password=password, Role='admin').first()
    if admin:
        session['user_id'] = admin.UserID
        session['username'] = admin.Username
        session['role'] = 'admin'
        flash('Admin Login Successful!', 'success')
        return redirect(url_for('admin_dashboard'))
    else:
        flash('Invalid Admin Credentials!', 'danger')
        return redirect(url_for('home'))
    

# -------------------------------- User login and sign up and logout -------------------------------- #

@app.route('/usersignup', methods=['POST'])
def usersignup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    fullname = request.form['fullname']
    qualification = request.form['qualification']
    dob = request.form['dob']  # This comes as a string from the form

    # Convert DOB from string to date object
    dob = datetime.strptime(dob, "%Y-%m-%d").date()

    existing_user = User.query.filter((User.Username == username) | (User.Email == email)).first()
    if existing_user:
        flash("Username or Email already exists!", "danger")
        return redirect(url_for("home"))

    new_user = User(
        Username=username, 
        Email=email, 
        Password=password,
        Fullname=fullname,
        Qualification=qualification,
        DOB=dob
    )

    db.session.add(new_user)
    db.session.commit()
    flash("User Registration Successful! Please Login.", "success")
    return redirect(url_for("home"))



@app.route('/userlogin', methods=['POST'])
def userlogin():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(Username=username, Password=password).first()
    if user:
        session['user_id'] = user.UserID
        session['username'] = user.Username
        session['role'] = user.Role
        flash("Login Successful!", "success")
        return redirect(url_for("admin_dashboard" if user.Role == "admin" else "user_dashboard"))
    else:
        flash("Invalid Credentials! Please try again or sign up.", "danger")
        return redirect(url_for("home"))

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged Out Successfully!", "info")
    return redirect(url_for("home"))



# -------------------------------- Admin and user Dashboard  -------------------------------- #


@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or session['role'] != 'admin':
        flash("Unauthorized Access!", "danger")
        return redirect(url_for("home"))

    users = User.query.all()
    subjects = Subject.query.all()
    quizzes = Quiz.query.all()
    chapters = Chapter.query.all()

    return render_template("admin_dashboard.html", users=users, subjects=subjects, quizzes=quizzes, chapters=chapters)

@app.route('/user_dashboard')
def user_dashboard():
    if 'user_id' not in session or session['role'] != 'user':
        flash("Unauthorized Access!", "danger")
        return redirect(url_for("home"))

    user = User.query.get(session['user_id'])

    # Fetch all subjects
    subjects = Subject.query.all()

    # Fetch all quizzes with associated chapters and subjects
    upcoming_quizzes = []
    for subject in subjects:
        chapters = Chapter.query.filter_by(SubjectID=subject.SubjectID).all()
        for chapter in chapters:
            quizzes = Quiz.query.filter_by(ChapterID=chapter.ChapterID).all()
            for quiz in quizzes:
                upcoming_quizzes.append({
                    'quiz': quiz,
                    'chapter': chapter,
                    'subject': subject
                })

    # Fetch past quiz scores
    scores = Score.query.filter_by(UserID=user.UserID).all()

    return render_template(
        "user_dashboard.html",
        user=user,
        upcoming_quizzes=upcoming_quizzes,
        scores=scores
    )


# -------------------------------- Admin Functionalities -------------------------------- #


                # CRUD Subject 

@app.route('/add_subject', methods=['POST'])
def add_subject():
    if 'user_id' not in session or session['role'] != 'admin':
        flash("Unauthorized Access!", "danger")
        return redirect(url_for("home"))

    subject_name = request.form['subject_name']
    description = request.form['description']

    # Create new subject
    new_subject = Subject(Subjectname=subject_name, Description=description)
    db.session.add(new_subject)
    db.session.commit()

    flash("New Subject Added Successfully!", "success")
    return redirect(url_for("admin_dashboard"))

# Edit Subject
@app.route('/edit_subject/<int:subject_id>', methods=['POST'])
def edit_subject(subject_id):
    if 'user_id' not in session or session['role'] != 'admin':
        flash("Unauthorized Access!", "danger")
        return redirect(url_for("home"))

    subject = Subject.query.get(subject_id)
    if subject:
        subject.Subjectname = request.form['subject_name']
        subject.Description = request.form['description']
        db.session.commit()
        flash("Subject Updated Successfully!", "success")

    return redirect(url_for("admin_dashboard"))

# Delete Subject
@app.route('/delete_subject/<int:subject_id>')
def delete_subject(subject_id):
    if 'user_id' not in session or session['role'] != 'admin':
        flash("Unauthorized Access!", "danger")
        return redirect(url_for("home"))

    subject = Subject.query.get(subject_id)
    if subject:
        db.session.delete(subject)
        db.session.commit()
        flash("Subject Deleted Successfully!", "success")

    return redirect(url_for("admin_dashboard"))


              #CRUD Chapter


@app.route('/add_chapter', methods=['POST'])
def add_chapter():
    if 'user_id' not in session or session['role'] != 'admin':
        flash("Unauthorized Access!", "danger")
        return redirect(url_for("home"))

    subject_id = request.form['subject_id']
    chapter_name = request.form['chapter_name']
    description = request.form['description']

    # Create new chapter
    new_chapter = Chapter(SubjectID=subject_id, Chaptername=chapter_name, Description=description)
    db.session.add(new_chapter)
    db.session.commit()

    flash("New Chapter Added Successfully!", "success")
    return redirect(url_for("admin_dashboard"))


# Edit Chapter
@app.route('/edit_chapter/<int:chapter_id>', methods=['POST'])
def edit_chapter(chapter_id):
    if 'user_id' not in session or session['role'] != 'admin':
        flash("Unauthorized Access!", "danger")
        return redirect(url_for("home"))

    chapter = Chapter.query.get(chapter_id)
    if chapter:
        chapter.Chaptername = request.form['chapter_name']
        chapter.Description = request.form['description']
        db.session.commit()
        flash("Chapter Updated Successfully!", "success")

    return redirect(url_for("admin_dashboard"))

# Delete Chapter
@app.route('/delete_chapter/<int:chapter_id>')
def delete_chapter(chapter_id):
    if 'user_id' not in session or session['role'] != 'admin':
        flash("Unauthorized Access!", "danger")
        return redirect(url_for("home"))

    chapter = Chapter.query.get(chapter_id)
    if chapter:
        db.session.delete(chapter)
        db.session.commit()
        flash("Chapter Deleted Successfully!", "success")

    return redirect(url_for("admin_dashboard"))


              # CRUD Quiz 


@app.route('/add_quiz', methods=['POST'])
def add_quiz():
    if 'user_id' not in session or session['role'] != 'admin':
        flash("Unauthorized Access!", "danger")
        return redirect(url_for("home"))

    chapter_id = request.form['chapter_id']
    date_of_quiz = request.form['date_of_quiz']
    time_duration = request.form['time_duration']
    remarks = request.form.get('remarks', '')

    # Create new quiz
    new_quiz = Quiz(
        ChapterID=chapter_id,
        Date_of_quiz=datetime.strptime(date_of_quiz, "%Y-%m-%d").date(),
        Time_duration=time_duration,
        Remarks=remarks
    )
    db.session.add(new_quiz)
    db.session.commit()

    flash("New Quiz Added Successfully!", "success")
    return redirect(url_for("admin_dashboard"))

@app.route('/edit_quiz/<int:quiz_id>', methods=['POST'])
def edit_quiz(quiz_id):
    if 'user_id' not in session or session['role'] != 'admin':
        flash("Unauthorized Access!", "danger")
        return redirect(url_for("home"))

    quiz = Quiz.query.get(quiz_id)
    if quiz:
        quiz.Date_of_quiz = datetime.strptime(request.form['date_of_quiz'], "%Y-%m-%d").date()
        quiz.Time_duration = request.form['time_duration']
        quiz.Remarks = request.form['remarks']
        db.session.commit()
        flash("Quiz Updated Successfully!", "success")
    else:
        flash("Quiz Not Found!", "danger")

    return redirect(url_for("admin_dashboard"))

@app.route('/delete_quiz/<int:quiz_id>', methods=['GET'])
def delete_quiz(quiz_id):
    if 'user_id' not in session or session['role'] != 'admin':
        flash("Unauthorized Access!", "danger")
        return redirect(url_for("home"))

    quiz = Quiz.query.get(quiz_id)
    if quiz:
        db.session.delete(quiz)
        db.session.commit()
        flash("Quiz Deleted Successfully!", "success")
    else:
        flash("Quiz Not Found!", "danger")

    return redirect(url_for("admin_dashboard"))

         #CRUD Question 

# Route to Add a New Question
@app.route('/add_question', methods=['POST'])
def add_question():
    if 'user_id' not in session or session['role'] != 'admin':
        flash("Unauthorized Access!", "danger")
        return redirect(url_for("home"))

    question_statement = request.form['question_statement']
    option1 = request.form['option1']
    option2 = request.form['option2']
    option3 = request.form['option3']
    option4 = request.form['option4']
    correct_option_index = request.form['correct_option']  # This will be 1, 2, 3, or 4
    quiz_id = request.form['quiz_id']

    # Mapping the correct option index to actual value
    correct_option = [option1, option2, option3, option4][int(correct_option_index) - 1]

    new_question = Questions(
        Question_statement=question_statement,
        Option1=option1,
        Option2=option2,
        Option3=option3,
        Option4=option4,
        Correct_option=correct_option,
        QuizID=quiz_id
    )

    db.session.add(new_question)
    db.session.commit()
    flash("New Question Added Successfully!", "success")
    return redirect(url_for("admin_dashboard"))


# Route to Edit a Question
@app.route('/edit_question/<int:question_id>', methods=['POST'])
def edit_question(question_id):
    if 'user_id' not in session or session['role'] != 'admin':
        flash("Unauthorized Access!", "danger")
        return redirect(url_for("home"))

    question = Questions.query.get(question_id)
    if not question:
        flash("Question not found!", "danger")
        return redirect(url_for("admin_dashboard"))

    question.Question_statement = request.form['question_statement']
    question.Option1 = request.form['option1']
    question.Option2 = request.form['option2']
    question.Option3 = request.form['option3']
    question.Option4 = request.form['option4']
    
    correct_option_index = request.form['correct_option']
    question.Correct_option = [question.Option1, question.Option2, question.Option3, question.Option4][int(correct_option_index) - 1]

    db.session.commit()
    flash("Question Updated Successfully!", "success")
    return redirect(url_for("admin_dashboard"))


# Route to Delete a Question
@app.route('/delete_question/<int:question_id>')
def delete_question(question_id):
    if 'user_id' not in session or session['role'] != 'admin':
        flash("Unauthorized Access!", "danger")
        return redirect(url_for("home"))

    question = Questions.query.get(question_id)
    if not question:
        flash("Question not found!", "danger")
    else:
        db.session.delete(question)
        db.session.commit()
        flash("Question Deleted Successfully!", "success")

    return redirect(url_for("admin_dashboard"))

# -------------------------------- User Functionalities --------------------------------- #





@app.route('/user_scores')
def user_scores():
    if 'user_id' not in session:
        flash("Unauthorized access!", "danger")
        return redirect(url_for("home"))

    user_id = session['user_id']
    scores = Score.query.filter_by(UserID=user_id).all()

    # Add a flag for retake eligibility
    for score in scores:
        score.retake_allowed = score.TotalScore < 40  # Check if score is below 40%

    return render_template("quiz_scores.html", scores=scores)



@app.route('/start_quiz/<int:quiz_id>')
def start_quiz(quiz_id):
    if 'user_id' not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for("home"))

    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Questions.query.filter_by(QuizID=quiz_id).all()

    if not questions:
        flash("No questions found for this quiz.", "danger")
        return redirect(url_for("user_dashboard"))

    session['quiz_id'] = quiz_id
    session['current_question'] = 0  # Start with the first question
    session['user_answers'] = {}  # Store user responses

    return redirect(url_for('next_question'))

@app.route('/next_question', methods=['POST', 'GET'])
def next_question():
    if 'quiz_id' not in session:
        flash("Quiz session expired. Please start again.", "danger")
        return redirect(url_for("user_dashboard"))

    quiz_id = session['quiz_id']
    current_question_index = session['current_question']
    questions = Questions.query.filter_by(QuizID=quiz_id).all()

    # If all questions are answered, redirect to submit
    if current_question_index >= len(questions):
        return redirect(url_for("submit_quiz", quiz_id=quiz_id))

    question = questions[current_question_index]
    total_questions = len(questions)
    quiz = Quiz.query.get(quiz_id)  # ✅ FIXED: Now passing quiz object

    return render_template(
        "quiz_attempt.html",
        quiz=quiz,
        quiz_id=quiz_id,
        question=question,
        current_question=current_question_index + 1,
        total_questions=total_questions,
    )


@app.route('/save_answer', methods=['POST'])
def save_answer():
    if 'quiz_id' not in session:
        flash("Quiz session expired. Please start again.", "danger")
        return redirect(url_for("user_dashboard"))

    selected_answer = request.form.get("selected_answer")
    question_id = request.form.get("question_id")

    if 'user_answers' not in session:
        session['user_answers'] = {}

    if question_id and selected_answer:
        session['user_answers'][str(question_id)] = selected_answer  # Ensure correct data type
    
    session.modified = True  # Ensure session updates are saved

    # Move to the next question
    session['current_question'] += 1

    # **Check if all questions are answered, then submit quiz**
    quiz_id = session['quiz_id']
    total_questions = Questions.query.filter_by(QuizID=quiz_id).count()

    if session['current_question'] >= total_questions:
        return redirect(url_for("submit_quiz", quiz_id=quiz_id))

    return redirect(url_for("next_question"))




@app.route('/submit_quiz/<int:quiz_id>', methods=['POST'])
def submit_quiz(quiz_id):
    if 'user_id' not in session:
        flash("Please log in to submit the quiz.", "danger")
        return redirect(url_for('home'))

    user_id = session['user_id']
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Questions.query.filter_by(QuizID=quiz_id).all()

    # ✅ Ensure last question's answer is saved
    last_question_id = request.form.get("question_id")
    last_answer = request.form.get("selected_answer")

    if 'user_answers' not in session:
        session['user_answers'] = {}

    if last_question_id and last_answer:
        session['user_answers'][str(last_question_id)] = last_answer  # ✅ Convert key to string

    session.modified = True  # ✅ Ensure session updates

    # ✅ Now, calculate the score correctly
    score = 0

    for question in questions:
        question_id = str(question.QuestionID)  # ✅ Ensure consistent data type
        submitted_answer = session['user_answers'].get(question_id, None)
        correct_answer = question.Correct_option

        if submitted_answer == correct_answer:
            score += 1  

    total_questions = len(questions)
    final_score = (score / total_questions) * 100

    print(f"DEBUG: User {user_id}, Correct Answers: {score}, Total Questions: {total_questions}, Final Score: {final_score}")

    # ✅ Save score in the database
    new_score = Score(QuizID=quiz_id, UserID=user_id, TotalScore=final_score)
    db.session.add(new_score)
    db.session.commit()

    # ✅ Store answers in `UserAnswers` table
    for question_id, selected_answer in session['user_answers'].items():
        new_answer = UserAnswers(
            ScoreID=new_score.ScoreID,
            QuestionID=int(question_id),  # ✅ Convert back to integer
            SelectedAnswer=selected_answer
        )
        db.session.add(new_answer)

    db.session.commit()

    # ✅ Clear session data after submission
    session.pop('quiz_id', None)
    session.pop('current_question', None)
    session.pop('user_answers', None)

    flash(f"Quiz submitted! Your score: {final_score:.2f}%", "success")
    return redirect(url_for('user_dashboard'))



@app.route("/")
def home():
    return render_template("index.html")



if __name__ == "__main__":
    create_admin()  # Ensures the admin exists before running Flask
    app.run(debug=True)