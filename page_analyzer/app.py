import os

from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')


@app.route('/')
def urls_index():
    return  'Hello!'