from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


#initializing the flask app 
app=Flask(__name__)
app.secret_key = "astitva"

#initialising the database
db=SQLAlchemy(app)


#-------------------------------- Models and Tables ----------------------------------------


class User(db.Model):
    __tablename__='user'
    UserID=db.Column(db.Integer , primary_key = True , autoincrement = True )
    Username=db.Column(db.String(500),nullable=False)
    Password = db.Column(db.String(500) , nullable=False)
    Fullname=db.Column(db.String(500) , nullable=False)
    Qualification=db.Column(db.String(500),nullable=False)
    DOB = db.Column(db.Date, nullable=False)


class Subject(db.Model):
    __tablename__='subject'
    SubjectID=db.Column(db.Integer , primary_key = True , autoincrement = True )
    Subjectname=db.Column(db.String(500),nullable=False)
    Description=db.Column(db.string(500),nullable=False)


class Chapter(db.Model):
    __tablename__='chapter'
    ChapterID=db.Column(db.Integer , primary_key = True , autoincrement = True )
    Chaptername=db.Column(db.String(500),nullable=False)
    Description=db.Column(db.string(500),nullable=False)

    QuizR=db.relationship('Quiz',backref='chapter' , lazy=True)

class Quiz(db.Model):
    __tablename__='quiz'
    QuizID=db.Column(db.Integer , primary_key = True , autoincrement = True )
    Date_of_quiz=db.Column(db.Date , nullable=False)
    Time_duration=db.Column(db.Time , nullable=False)
    Remarks=db.Column(db.String(500))

    ChapterID=db.Column(db.Integer , db.ForeignKey('chapter.ChapterID') , nullable=False )

    QuestionsR=db.relationship('Questions',backref='quiz' , lazy=True)



class Questions(db.Model):
    __tablename__='questions'
    QuestionID=db.Column(db.Integer , primary_key = True , autoincrement = True )
    Question_statement=db.Column(db.String(500) , nullable=False)
    Option1=db.Column(db.String(500) , nullable=False)
    Option2=db.Column(db.String(500) , nullable=False)
    Option3=db.Column(db.String(500) , nullable=False)
    Option4=db.Column(db.String(500) , nullable=False)
    Correct_option=db.Column(db.String(500) , nullable=False)

    QuizID=db.Column(db.Integer , db.ForeignKey('quiz.QuizID') , nullable=False )
  





#home route 
@app.route("/")
def home():
    return render_template("index.html") 

#running the application 
if __name__ == "__main__":
    app.run(debug=True)
    

