"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, flash, session, redirect

import hackbright

app = Flask(__name__)

app.secret_key = "SEEEECCREEEET"

@app.route("/")
def show_homepage():
    projects = hackbright.get_all_projects()
    githubs = hackbright.get_all_students()
    return render_template("home.html", projects=projects, githubs=githubs)

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)
    grades = hackbright.get_grades_by_github(github)

    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           grades=grades)

    return html


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student"""

    return render_template("student_search.html")


@app.route("/student-add")
def get_student_add_form():
    """Show form for searching for a student"""

    return render_template("student_add.html")


@app.route("/student-add", methods=['POST'])
def add_student():
    """Add a student"""
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)
    flash(f"{first_name} added")

    return redirect("/student-search")

@app.route("/project-search")
def get_project_form():

    return render_template("project_search.html")


@app.route("/project")   
def get_project():
    title = request.args.get('title')
    project = hackbright.get_project_by_title(title)
    grades = hackbright.get_grades_by_title(title)

    return render_template("project_info.html", project=project, grades=grades)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
