from flask import Flask, render_template, json, request
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Result


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/admin')
def showAddBlog():
    return render_template('admin.html')


if __name__ == '__main__':
    app.run()