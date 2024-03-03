from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired


class RegistrationForm(FlaskForm):
   
    first_name = StringField("First Name:", validators=[InputRequired()])
    last_name = StringField("Last Name:", validators=[InputRequired()])
    email = EmailField("Email:", validators=[InputRequired()])
    username = StringField("Username:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])


class loginForm(FlaskForm):
    username = StringField("username:", validators=[InputRequired()])
    password = PasswordField("password:", validators=[InputRequired()])
