from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///flaskTodo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# model


class Todo(db.Model):
    sNo = db.Column(db.Integer, primary_key=True)
    todoTitle = db.Column(db.String(200), nullable=False)
    todoDesc = db.Column(db.String(500), nullable=False)
    created_At = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f'{self.todoTitle} {self.created_At}'


@app.route("/", methods=['GET', 'POST'])
def index():
    title = 'Homepage'
    if request.method == 'POST':
        postTitle = request.form['title']
        postDescription = request.form['desc']
        todo = Todo(todoTitle=postTitle, todoDesc=postDescription)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo, title=title)

# edit todo


@app.route("/edit/<int:sNo>", methods=['GET', 'POST'])
def edit(sNo):
    if request.method == 'POST':
        postTitle = request.form['title']
        postDescription = request.form['desc']
        todo = Todo.query.filter_by(sNo=sNo).first()
        todo.todoTitle = postTitle
        todo.todoDesc = postDescription
        db.session.add(todo)
        db.session.commit()
    todo = Todo.query.filter_by(sNo=sNo).first()

    return render_template('edit.html', todo=todo)


@app.route('/delete/<int:sNo>')
def delete(sNo):
    deleteTodo = Todo.query.filter_by(sNo=sNo).first()
    db.session.delete(deleteTodo)
    db.session.commit()
    return redirect('/')


@app.route("/alltodos")
def todos():
    title = 'All-Todos'
    allTodo = Todo.query.all()
    return render_template('alltodos.html', allTodo=allTodo, title=title)


if __name__ == "__main__":
    app.run(debug=True)
