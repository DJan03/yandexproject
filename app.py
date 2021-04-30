from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
db = SQLAlchemy(app)


class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    voted_yes = db.Column(db.Integer, default=0)
    voted_no = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"Problem({self.id})"


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        problem_content = request.form["content"]
        new_problem = Problem(content=problem_content)

        try:
            db.session.add(new_problem)
            db.session.commit()
            return redirect('/')
        except:
            return "Problem with problem add"
    else:
        problems = Problem.query.order_by(Problem.date_created).all()
        return render_template("index.html", problems=problems)


@app.route("/delete/<int:id>")
def delete(id):
    problem_to_delete = Problem.query.get_or_404(id)

    try:
        db.session.delete(problem_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "Problem to delete problem"


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    problem = Problem.query.get_or_404(id)

    if request.method == "POST":
        problem.content = request.form["content"]

        try:
            db.session.commit()
            return redirect("/")
        except:
            return "Error"
    else:
        return render_template("update.html", problems=problems)


if __name__ == "__main__":
    app.run(debug=True)
