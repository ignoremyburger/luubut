from flask import Blueprint, render_template, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired
from flask_login import login_user, logout_user, current_user

from server.models import db, Users

from uuid import uuid1
from datetime import datetime
from hashlib import sha256

# Form
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField()

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField()

# Create Blueprint
authbp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="templates", static_folder="static")

# Routes
@authbp.route('/login', methods=['GET', 'POST'])
def login_route():
    if current_user.is_authenticated:
        return redirect('/dash')
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(
            username=form.username.data.strip(),
            password=sha256(form.password.data.encode()).hexdigest()
        ).first()
        if not user:
            flash("Sai tên đăng nhập hoặc tên người dùng", 'error')
            return redirect('/auth/login')
        login_user(user)
        return redirect('/dash')
    return render_template("login.html", form=form)

@authbp.route('/register', methods=['GET', 'POST'])
def register_page():
    if current_user.is_authenticated:
        return redirect('/dash')
    form = RegisterForm()
    if form.validate_on_submit():
        user_exist = Users.query.filter_by(username=form.username.data.strip()).first()
        if user_exist:
            flash("Đã có người dùng tồn tại với tên này", 'error')
            return redirect('/auth/register')
        if len(form.username.data) < 8:
            flash("Tên người dùng cần nhiều hơn 8 ký tự", 'error')
            return redirect('/auth/register')
        if len(form.password.data) < 8:
            flash("Mật khẩu cần nhiều hơn 8 ký tự", 'error')
            return redirect('/auth/register')
        user = Users(
            username=form.username.data.strip(),
            password=sha256(form.password.data.encode()).hexdigest(),
            user_id=str(uuid1()),
            creation_date=datetime.now().replace(microsecond=0),
            profile_picture=f"https://api.dicebear.com/8.x/thumbs/svg?seed={sha256(form.username.data.strip().encode()).hexdigest()}"
        )
        db.session.add(user)
        db.session.commit()
        flash("Đã tạo người dùng, đăng nhập lại nhé!", 'success')
        return redirect('/auth/login')
    return render_template("register.html", form=form)

@authbp.route('/logout', methods=['GET'])
def logout_page():
    logout_user()
    return redirect('/')