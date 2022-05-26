from flask import render_template, request, session, redirect, flash
from flask_app.models import user, test, question
from flask_app import app

@app.route('/questions/create', methods=['POST'])
def create_question():
    if "user_id" not in session:
        return redirect('/')
    if not question.Question.validate_question(request.form):
        flash("There needs to be at least 10 characters", "question")
        redirect('/dashboard')
    data = {
        "comment": request.form["comment"],
        "user_id": session["user_id"]
    }
    session["question_id"] = question.Question.create_question(data)
    return redirect('/dashboard')

@app.route('/questions/update/<int:question_id>', methods=['POST'])
def update_question(question_id):
    if not question.Question.validate_question(request.form):
        return redirect(f'/questions/edit/{question_id}')
    data = {
        "id": question_id,
        "comment": request.form["comment"],
        "user_id": session["user_id"]
    }
    question.Question.update_question(data)
    return redirect('/dashboard')
    # return redirect(f'/questions/edit/{question_id}')

@app.route('/questions/edit/<int:question_id>')
def edit_question(question_id):
    user_data = {
        "id": session["user_id"]
    }
    data = {                                                           
        "id": question_id,
    }
    print(question.Question.get_by_id(data))
    return render_template("edit.html", logged_in_user = user.User.get_by_id(user_data), this_question = question.Question.get_by_id_detailed(data))

@app.route('/questions/delete/<int:question_id>')
def destroy_question(question_id):
    data = {                                                           
        "id": question_id
    }
    question.Question.destroy_question(data)
    return redirect('/dashboard')