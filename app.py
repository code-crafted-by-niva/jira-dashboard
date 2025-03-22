from flask import Flask, render_template, redirect, url_for, Blueprint, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import bcrypt

#custom functions
from charts import *
import db


#import blueprint requirements
from dashboard import dashboard_blueprint

app = Flask(__name__)
app.secret_key = "jdgfwilrgfifguweifqE"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'


class User(UserMixin):
    def __init__(self, name, email):
        self.id = email
        self.name = name

@login_manager.user_loader
def load_user(user_id):
    user = db.get_user_details(user_id)
    if user:
        return User(name=user["name"],email=user["email"])
    return None


#Register Blueprint
app.register_blueprint(dashboard_blueprint)

#Register charts 
app.jinja_env.globals.update(
    get_issue_length = get_issue_length,
    get_issues_trends = get_issues_trends,
    get_colour = get_colour,
    get_issue_status_count = get_issue_status_count)

@app.route('/')
def home():
    page = {"title"   : "Home",
            "icon"    : "fa fa-home",
            "heading" : "Home",
            "desc"    : "Welcome to JIRA Dashboard"}
    
    return render_template('/pages/home.html',page=page)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    print("inside sign up")
    #check if user has already signed in
    if current_user.is_authenticated:
        flash('User already signed in.','success')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        print("inside post")
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        print("form values : ",name,email,password)
        if db.get_user_details(email):
            flash('Email already exist. Please sign in','warning')
            return redirect(url_for('signin'))
        
        db.insert_user_details(name, email, password)
        user_obj = User(name=name,email=email)
        print("user created")
        login_user(user_obj)
        print("user signup")
        flash('Signup successful ! please enter your JIRA details','success')
        return redirect(url_for('home'))
    
    return render_template('/authentication/signup.html',
                           page={'title':'Sign Up'})    


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = db.get_user_details(email)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            user_obj = User(name=user["name"],email=email)
            login_user(user_obj)
            #flash('Login Successful', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('/authentication/signin.html',
                           page={'title':'Sign In'})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out Successful', 'success')
    return redirect(url_for('signin'))




@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    page = {"title"   : "JIRA Settings",
            "icon"    : "fas fa-cogs",
            "heading" : "JIRA Credentials Settings",
            "desc"    : "Provide JIRA credentials & url for connecting with dashboard"}
    jira_details = {
            "uid" : current_user.id,
            "type"  : "",
            "url"   : "",
            "email" : "",
            "token" : ""
        }
    if request.method == 'POST':
        jira_details = {
            "uid" : current_user.id,
            "type"  : request.form.get('type'),
            "url"   : request.form.get('url'),
            "email" : request.form.get('email'),
            "token" : request.form.get('token')
        }
        print("Email",jira_details)
        db.update_jira_details(jira_details)
        flash('JIRA details updated successfully', 'success')
        return redirect(url_for('settings'))
    print(current_user.id, request.args.get('type', 'default'))
    jira_details = db.get_jira_details(current_user.id, version="JIRA Cloud")
    
    return render_template('/pages/settings.html',
                           page = page,
                           jira_details=jira_details)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    page = {"title"   : "Profile",
            "icon"    : "fa fa-user",
            "heading" : "Profile",
            "desc"    : "Manage your JIRA Dashboard Profile"}

    user_details = db.get_user_details(current_user.id)

    return render_template('/pages/profile.html',page=page, user_details=user_details)

    


if __name__ == "__main__":
    app.run(debug=True,port=8080)
