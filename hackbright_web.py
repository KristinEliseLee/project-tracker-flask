"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, flash, session, redirect

import hackbright

app = Flask(__name__)

app.secret_key = "SEEEECCREEEET"

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github)

    return html


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student"""

    return render_template("student_search.html")


@app.route("/student-add")
def get_student_add_form():
    """Show form for searching for a student"""

    return render_template("add_student.html")



@app.route("/student-added", methods=['Post'])
def add_student():
    """Add a student"""
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)
    flash(f"{first_name} added")

    return redirect("/student-search")


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
