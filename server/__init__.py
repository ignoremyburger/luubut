from flask import Flask
from dotenv import load_dotenv
import os

# Create app
app = Flask(__name__)
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB')
app.config['SECRET_KEY'] = os.getenv('SECRET')

# User Loader
from flask_login import LoginManager
from server.models import db, Users

# Create Database
with app.app_context():
    db.create_all()

lm = LoginManager(app)
lm.login_view = "auth.login_route"
lm.login_message = "Bạn cần đăng nhập trước khi tiếp tục"
lm.login_message_category = "warning"

@lm.user_loader
def load_user(id):
    return Users.query.get(int(id))

# Register Blueprints
from server.routes.index import indexbp
from server.routes.auth import authbp
from server.routes.dashboard import dashbp

app.register_blueprint(indexbp)
app.register_blueprint(authbp)
app.register_blueprint(dashbp)

