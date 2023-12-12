from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(application)

# Add the following line to create the engine with additional arguments
engine = create_engine('sqlite:///mydatabase.db', connect_args={'check_same_thread': False}, module=sqlite, module_args={'version': '3.8.3'})

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

@application.route('/')
def index():
    notes = Note.query.all()
    return render_template('index.html', notes=notes)

@application.route('/add_note', methods=['POST'])
def add_note():
    title = request.form['title']
    content = request.form['content']
    new_note = Note(title=title, content=content)
    db.session.add(new_note)
    db.session.commit()
    return redirect(url_for('index'))

@application.route('/edit_note/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    note = Note.query.get(id)
    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', note=note)

@application.route('/delete_note/<int:id>')
def delete_note(id):
    note = Note.query.get(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with application.app_context():
        db.create_all()
    application.run(debug=True)
    application.run(host='0.0.0.0', port=8000)