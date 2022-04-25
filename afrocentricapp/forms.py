from re import M
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField

from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    username = StringField("Your Email", validators=[DataRequired(),Email()])

    password = PasswordField("Enter your password")

    submitbtn = SubmitField("Login")