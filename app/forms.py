from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit1 = SubmitField('Log In')

class SignInForm(FlaskForm):
    username = StringField('UsernameSignUp', validators=[DataRequired()])
    password = PasswordField('PasswordSignUp', validators=[DataRequired()])
    submit2 = SubmitField('Sign Up')