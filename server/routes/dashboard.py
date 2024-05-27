from flask import Blueprint, render_template, redirect, flash, request
from flask_wtf import FlaskForm
from wtforms import FileField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, DataRequired
from flask_login import login_required, current_user

from server.models import db, Users, Notes

import requests

# Create Blueprint
dashbp = Blueprint("dash", __name__, url_prefix="/dash", template_folder="templates", static_folder="static")

# Forms
class UpdateAppreciation(FlaskForm):
    thank_you_note = TextAreaField(validators=[InputRequired()])
    submit = SubmitField()

class UpdateAvatar(FlaskForm):
    avatar = FileField(validators=[DataRequired()])
    submit = SubmitField()

# Routes
@dashbp.route('/', methods=['GET'])
@login_required
def dashboard_page():
    notes = Notes.query.filter_by(user=current_user.id).all()
    return render_template("dash.html", notes=notes, share_link=f"{request.root_url}send/{current_user.username}", note_count=len(notes), update_appreciation=UpdateAppreciation(), update_avatar=UpdateAvatar())

@dashbp.route('/update-appreciation', methods=['POST'])
@login_required
def update_appreciation():
    form = UpdateAppreciation()
    if form.validate_on_submit():
        user = Users.query.filter_by(id=current_user.id).first()
        user.thank_you_note = form.thank_you_note.data
        db.session.commit()
        flash("Đã cập nhật lời cảm ơn", 'success')
        return redirect('/dash')
    return redirect('/dash')

@dashbp.route('/update-avatar', methods=['POST'])
@login_required
def update_avatar():
    form = UpdateAvatar()
    if form.validate_on_submit():
        data = form.avatar.data
        if data:
            # Check File extension
            if data.filename.split('.')[-1] not in ['jpg', 'jpeg', 'png']:
                flash(f"Chúng mình không hỗ trợ file {data.filename.split('.')[-1]}", 'error')
                return redirect('/dash')
            else:
                r = requests.post(
                    "https://freeimage.host/api/1/upload?key=6d207e02198a847aa98d0a2a901485a5&format=json",
                    files={'source': (data.filename, data.read())}
                )
                if r.status_code != 200:
                    flash(f"Không thể liên lạc với ImgCDN với status code {r.status_code}", 'error')
                    return redirect('/dash')
                user = Users.query.filter_by(id=current_user.id).first()
                user.profile_picture = r.json()['image']['url']
                db.session.commit()
                flash("Đã cập nhật ảnh đại diện", 'success')
                return redirect('/dash')
    return redirect('/dash')

