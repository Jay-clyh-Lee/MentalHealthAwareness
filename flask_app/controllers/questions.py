from flask import render_template, request, session, redirect, flash
from flask_app.models import user, question
from flask_app import app

@app.route('/questions/create', methods=['POST'])
def ask():
    if "user_id" not in session:
        return redirect('/')
    if not question.Question.validate(request.form):
        flash("There needs to be at least 50 characters", "question")
        redirect('/dashboard')
    data = {
        "question": request.form["question"],
        "user_id": session["user_id"]
    }
    question.Question.save(data)
    return redirect('/dashboard')

@app.route('/questions/update/<int:question_id>', methods=['POST'])
def update(question_id):
    if not question.Question.validate(request.form):
        return redirect(f'/questions/edit/{question_id}')
    data = {
        "question": request.form["question"],
        "user_id": session["user_id"]
    }
    question.Question.update(data)
    return redirect('/question/edit/<int:question_id>')

@app.route('/questions/edit/<int:question_id>')
def edit(question_id):
    user_data = {
        "id": session["user_id"]
    }
    data = {                                                           
        "id": question_id,
    }
    return render_template("edit.html", logged_in_user = user.User.get_by_id(user_data), question = question.Question.get_by_id(data))