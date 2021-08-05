from enum import unique
from todo_list import db
from flask_login import UserMixin
from todo_list import login
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    email_address = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    items = db.relationship('Todo_Item', backref='user', lazy='dynamic')

    def __repr__(self):
        return self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.user_id


class Todo_Item(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    todo_item = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __repr__(self):
        return self.todo_item


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))