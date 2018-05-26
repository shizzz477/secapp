from flask import flash, redirect, url_for, render_template, request, json
from app import app, securedb
from app.forms import LoginForm, RegisterForm

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        securedb.adduser(form.username.data,form.password.data)
        flash("Registration Completed")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = json.dumps({'username': form.username.data})
        if securedb.checkpassword(form.username.data,form.password.data):
            return redirect(url_for('index',user=u))
        else:
            flash('Username or password is invalid')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/')
@app.route('/index')
def index():
    sessionuser = request.args.get('user')
    if not sessionuser:
        sessionuser = {'username': 'Guest'}
        messages = [
            {
                'body': 'Welcome to the Super Secure Application'
            },
            {
                'body': 'Please Register and sign in'
            }
        ]
    else:
         sessionuser = json.loads(sessionuser)
         messages = [{'body': "You are logged in!!!"}]

    return render_template('index.html', title='Home', user=sessionuser, msgs=messages)
