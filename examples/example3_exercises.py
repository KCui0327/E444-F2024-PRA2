from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)
moment = Moment(app)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())

@app.route('/user/<user_name>')
def user(user_name):
    return render_template('user.html', name=user_name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500