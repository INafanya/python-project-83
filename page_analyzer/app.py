import os

from flask import Flask, render_template


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')


@app.route('/')
def index():
    return render_template(
        'index.html'
    )