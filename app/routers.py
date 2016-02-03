from app import app
#render_template gives you access to Jinja2 template engine
from flask import render_template, request, make_response, flash, redirect, session
from app.forms import LoginForm, RegisterForm, FriendForm
from app import db
from app.db_models import Users, Friends

@app.route('/',methods=['GET','POST'])
def index():
    login = LoginForm()
    # Check if get method
    if request.method == 'GET':
            return render_template('login.html',form=login,isLogged=False)
    else:
        # Check if form data is valid
        if login.validate_on_submit():
            user = Users.query.filter_by(email=login.email.data).filter_by(passw=login.passw.data)
            if user.count() == 1:
                session['user_id'] = user[0].id
                session['isLogged'] = True
                print(user)
                friends = Friends.query.filter_by(user_id=user[0].id)
                print(friends)
                return render_template('friends.html',isLogged=True,friends=friends)
            else:
                flash('Wrong username or password!')    
                return render_template('login.html',form=login,isLogged=False)
        # form data was not valid    
        else:
            flash('Give proper information to email and password fields!')
            return render_template('login.html',form=login,isLogged=False)

@app.route('/register',methods=['GET','POST'])
def register():
    newuser = RegisterForm()
        # Check if get method
    if request.method == 'GET':
        return render_template('register.html',form=newuser)
    else:
        if newuser.validate_on_submit():
            user = Users(newuser.email.data, newuser.passw.data)
            try:
                db.session.add(user)
                db.session.commit()
            except:
                db.session.rollback()
                flash('Username already in use')
                return render_template('register.html',form=newuser)
            flash('User {0} registered!'.format(newuser.email.data))            
            return redirect('/')
        else:
            flash('Check fields!')
            return render_template('register.html',form=newuser)

@app.route('/friends')
def friends():
    if not('isLogged' in session) or (session['isLogged'] == False):
        return redirect('/')
    else:
        friend = Users.query.get(session['user_id'])
        return render_template('friends.html',isLogged=True,friends=friend.friends)

    
@app.route('/addfriend',methods=['GET','POST'])
def addfriend():
    newfriend = FriendForm()
        # Check if get method
    if request.method == 'GET':
        return render_template('addfriend.html',form=newfriend,isLogged=True)
    else:
        if newfriend.validate_on_submit():
            # first solution below without db.relationship 
            friends = Friends(newfriend.name.data, newfriend.address.data, newfriend.age.data, session['user_id'])
            # second solution with db.relationship
            # friend = Users.query.get(session['user_id'])
            # print(friend.friends)            
            db.session.add(friends)
            db.session.commit()
            flash('New friend, {0} added to list!'.format(newfriend.name.data))            
            #return render_template('friends.html',isLogged=True,friends=friend.friends)
            return render_template('friends.html',isLogged=True,friends=friends)
        else:
            flash('Check fields!')
            return render_template('addfriend.html',form=newfriend,isLogged=True)

@app.route('/logout')
def logout():
    #delete user session (clear all values)
    session.clear()
    return redirect('/')
        
@app.route('/user/<user>')
def user(user):
    return render_template('friends.html',name=user)

#Example how you can define route methods
@app.route('/user',methods=['GET','POST'])
def userParams():
    name = request.args.get('name')
    agent = request.headers.get('User-Agent')
    preflang = request.headers.get('Accept-Language')
    return render_template('template_user.html',name=name,browser=agent,preflang=preflang)
