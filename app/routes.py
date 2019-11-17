from app import app
from flask import Flask, render_template, flash, redirect
from app.forms import LoginForm, SignInForm

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form_log_in = LoginForm()
    if form_log_in.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form_log_in.username.data, form_log_in.remember_me.data))
        return redirect('/')
    return render_template('login.html', title='Log In', form=form_log_in)

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    form_sign_up = SignInForm()
    print(form_sign_up.password.data)
    print(form_sign_up.password2.data)
    if form_sign_up.validate_on_submit() and form_sign_up.password.data == form_sign_up.password2.data:
        flash('Sign up requested for user{}'.format(form_sign_up.username.data))
        return redirect('/')
    return render_template('signup.html', title='Sign Up', form=form_sign_up)
