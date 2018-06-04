from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt =Bcrypt(app)


from form import LoginForm, RegisterForm, MessageForm
from models import Result, User, BlogPost





@app.route('/', methods=['GET', 'POST'])
# @login_required
def home():
    error = None
    form = MessageForm(request.form)
    if form.validate_on_submit():
        new_message = BlogPost(
            form.title.data,
            form.description.data,
            current_user.id
        )
        db.session.add(new_message)
        db.session.commit()
        flash('New entry was successfully posted. Thanks.')
        return redirect(url_for('home'))
    else:
        posts = db.session.query(BlogPost).all()
        return render_template('hello.html', posts=posts, form=form, error=error)


@app.route('/welcome')
# @login_required
def welcome():
    return render_template('hello.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    error = None
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name = request.form['username']).first() #search in db user
            if user is not None and \
            bcrypt.check_password_hash(user.password,request.form['password']):
                #session['logged_in'] = True
                login_user(user)#check if login instead using session
                flash('You were logged in.')
                return redirect(url_for('home'))
            else:
                error = 'Invalid Credentials. Please try again.'
                render_template('login.html', form=form,error=error)
    return render_template('login.html', form=form,error=error)


@app.route('/logout')
# @login_required
def logout():
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('home'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            name=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("You were successfully registered")
        return redirect(url_for('home'))
    return render_template('register.html', form=form)



@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()



if __name__ == "__main__":
    app.run(debug=True)
