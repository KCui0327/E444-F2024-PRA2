from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
moment = Moment(app)
bootstrap = Bootstrap(app)

class Form(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT Email Address?', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        valid = True
        err_msg = ""
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(regex, field.data):
            valid = False
            err_msg += 'Email is not a valid email address. '
        
        if 'utoronto' not in field.data:
            valid = False
            err_msg += 'Email must be a UofT email address.'

        if not valid:
            raise ValidationError(err_msg)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        old_email=session.get('email')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')
        session['name'] = form.name.data
        session['email'] = form.email.data

        return redirect(url_for('index'))
    
    if form.name.data:
        session['name'] = form.name.data
    
    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'))

@app.route('/user/<user_name>')
def user(user_name):
    return render_template('user.html', name=user_name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500