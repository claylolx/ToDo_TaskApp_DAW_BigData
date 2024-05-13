from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definicion de una clase llamada TodoItem que hereda de db.Model, que es la clase base de SQLAlchemy para definir modelos de bases de datos.
class TodoItem(db.Model): # Clase hecha con CHATGPT
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<TodoItem {self.id}>'

# Rutas para FLASK acciones CRUD
@app.route('/')
def index():
    todo_items = TodoItem.query.all()
    return render_template('index.html', todo_items=todo_items)

@app.route('/add', methods=['POST'])
def add_todo():
    content = request.form['content']
    new_todo = TodoItem(content=content, created_at=datetime.now())
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<int:todo_id>')
def complete_todo(todo_id):
    todo = TodoItem.query.get(todo_id)
    todo.completed = True
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    todo = TodoItem.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit_todo(todo_id):
    todo = TodoItem.query.get(todo_id)
    if request.method == 'POST':
        todo.content = request.form['content']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', todo=todo)

@app.route('/uncomplete/<int:todo_id>')
def uncomplete_todo(todo_id):
    todo = TodoItem.query.get(todo_id)
    todo.completed = False
    db.session.commit()
    return redirect(url_for('index'))

# Crear base de datos y ejecutar aplicación
if __name__ == '__main__':
    with app.app_context(): # Contexto de flask para iniciar la base de datos
        db.create_all()     # Crea las tablas definidas en el modelo SQLAlchemy
    app.run(debug=True)     # Cada cambio se recarga sin necesidad de reiniciar el programa