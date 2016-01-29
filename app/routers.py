from app import app
#render_template gives you access to Jinja2 template engine
from flask import render_template, request, make_response, flash, redirect
from app.forms import LoginForm, RegisterForm
from app import db
from app.db_models import Users

@app.route('/',methods=['GET','POST'])
def index():
    login = LoginForm()
    # Check if get method
    if request.method == 'GET':
        return render_template('login.html',form=login)
    else:
        # Check if form data is valid
        if login.validate_on_submit():
            print (login.email.data)
            print (login.passw.data)
            return render_template('template_user.html')
        # form data was not valid    
        else:
            flash('Give proper information to email and password fields!')
            return render_template('login.html',form=login)

@app.route('/register',methods=['GET','POST'])
def register():
    newuser = RegisterForm()
        # Check if get method
    if request.method == 'GET':
        return render_template('register.html',form=newuser)
    else:
        if newuser.validate_on_submit():
            user = Users(newuser.email.data, newuser.passw.data)
            db.session.add(user)
            db.session.commit()
            flash('User {0} registered!'.format(newuser.email.data))            
            return redirect('/')
        else:
            flash('Check fields!')
            return render_template('register.html',form=newuser)
    
@app.route('/user/<user>')
def user(user):
    return render_template('template_user.html',name=user)

#Example how you can define route methods
@app.route('/user',methods=['GET','POST'])
def userParams():
    name = request.args.get('name')
    agent = request.headers.get('User-Agent')
    preflang = request.headers.get('Accept-Language')
    return render_template('template_user.html',name=name,browser=agent,preflang=preflang)