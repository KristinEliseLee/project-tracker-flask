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

    return redirect("/")


@app.route("/project-add")
def get_project_add_form():
    """Show form for adding a project"""

    return render_template("project_add.html")


@app.route("/project-add", methods=['POST'])
def add_project():
    """Add a project"""
    title = request.form.get('title')
    description = request.form.get('description')
    max_grade = request.form.get('max_grade')
    hackbright.make_new_project(title, description, max_grade)
    flash(f"{title} added")

    return redirect("/")


@app.route("/project-search")
def get_project_form():

    return render_template("project_search.html")


@app.route("/project")
def get_project():
    title = request.args.get('title')
    project = hackbright.get_project_by_title(title)
    grades = hackbright.get_grades_by_title(title)

    return render_template("project_info.html", project=project, grades=grades)


@app.route("/assign-grade")
def get_assign_grade_form():
    titles = hackbright.get_all_projects()
    githubs = hackbright.get_all_students()

    return render_template("assign_grade.html", titles=titles, githubs=githubs)


@app.route("/assign-grade", methods=['POST'])
def assign_grade():
    title = request.form.get('title')
    github = request.form.get('github')
    grade = request.form.get('grade')

    current_grade = hackbright.get_grade_by_github_title(github, title)

    if not current_grade:
        hackbright.assign_grade(github, title, grade)
        flash(f"Grade added")
    else:
        hackbright.update_grade(github, title, grade)
        flash(f"Grade updated")

    return redirect('/')


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
