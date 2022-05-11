from flask import Blueprint, jsonify,render_template,request
from flask_login import login_required,current_user
from website.models import Notes
from website import db
import json

views = Blueprint('views',__name__)

@views.route('/',methods = ['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form['Textarea']
        add_note = Notes(note = note,user_id = current_user.id)
        db.session.add(add_note)
        db.session.commit()
    return render_template("home.html" , users = current_user)

@views.route('/deletenote', methods = ['POST'])
def deleteNote():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Notes.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})