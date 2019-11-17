from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit1 = SubmitField('Log In')

class SignInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=32)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=32)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), Length(max=32)])
    city = StringField('City', validators=[DataRequired(), Length(max=32)])
    region = StringField('Region', validators=[DataRequired(), Length(max=32)])
    submit2 = SubmitField('Sign Up')