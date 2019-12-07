from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit1 = SubmitField('Log In')

class SignInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=128)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), Length(max=128)])
    city = StringField('City', validators=[DataRequired(), Length(max=64)])
    region = StringField('Region', validators=[DataRequired(), Length(max=64)])
    submit2 = SubmitField('Sign Up')

class FriendForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit3 = SubmitField('Add Friend')