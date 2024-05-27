from flask import Blueprint, render_template, redirect, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from flask_login import current_user
from wtforms.validators import InputRequired

from server.models import db, Users, Notes

from uuid import uuid1
from datetime import datetime

# Create Blueprint
indexbp = Blueprint("index", __name__, url_prefix="/", template_folder="templates", static_folder="static")

# Forms
class SendNote(FlaskForm):
    note_sender = StringField(validators=[InputRequired()])
    note_content = TextAreaField(validators=[InputRequired()])
    submit = SubmitField()

# Routes
@indexbp.route('/', methods=['GET'])
def index_page():
    return render_template("index.html")

@indexbp.route('/send/<username>', methods=['GET', 'POST'])
def send_to_user(username):
    if current_user.is_authenticated and current_user.username == username:
        flash("Bạn không thể tự gửi lưu bút cho chính mình!", 'error')
        return redirect('/')
    form = SendNote()
    user = Users.query.filter_by(username=username.strip()).first()
    if not user:
            flash('Ấy! Người dùng đó không tồn tại. Kiểm tra lại nhé!', 'error')
            return redirect('/')
    if form.validate_on_submit():
        note_count = Notes.query.filter_by(user=user.id).count()
        if note_count > user.note_max:
            flash('Người dùng này đã quá hạn mức số lượng lưu bút!', 'error')
            return redirect('/')
        if len(form.note_content.data) > 150:
            flash("Lưu bút của bạn vượt quá 150 ký tự!", 'error')
            return redirect(f'/send/{username}')
        n = Notes(
            user=user.id,
            sender=form.note_sender.data,
            note_id=str(uuid1().hex),
            note_content=form.note_content.data,
            creation_date=datetime.now().replace(microsecond=0)
        )
        db.session.add(n)
        db.session.commit()
        flash(f'Đã gửi lưu bút cho {username}!', 'success')
        return redirect(f'/send/{username}/success')
    return render_template("send.html", form=form, user=user)

@indexbp.route('/send/<username>/success', methods=['GET'])
def send_to_user_success(username):
    user = Users.query.filter_by(username=username.strip()).first()
    if not user:
        flash('Ấy! Người dùng đó không tồn tại. Kiểm tra lại nhé!', 'error')
        return redirect('/')
    return render_template("send-success.html", user=user)