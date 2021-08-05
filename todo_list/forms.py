from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators
from todo_list.models import User

class Registration_Form(FlaskForm):
    username = StringField('Username:', validators=[validators.DataRequired(), validators.Length(min=3, max=15)])
    email_address = StringField('Email-Address:', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Password:', validators=[validators.DataRequired()])
    password2 = PasswordField('Confirm Password:', validators=[validators.DataRequired(), validators.EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise validators.ValidationError('Username already taken')

    def validate_email_address(self, email_address):
        user = User.query.filter_by(email_address=email_address.data).first()
        if user is not None:
            raise validators.ValidationError('Email is already registered')


class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[validators.DataRequired()])
    password = PasswordField('Password:', validators=[validators.DataRequired()])
    remember_me = BooleanField('Remeber Me')
    submit = SubmitField('Login')

class Item_Form(FlaskForm):
    item_title = StringField(validators=[validators.DataRequired()])
    submit = SubmitField('Submit')

class Edit_Item_Form(FlaskForm):
    new_item_title = StringField(validators=[validators.DataRequired()])
    submit = SubmitField('Edit')
