from flask import Blueprint, session, redirect, request, render_template, flash, url_for
from app.forms import FriendForm
from app import db
from app.db_models import Users
from app.db_models import Friends
from werkzeug import secure_filename

# Create blueprint
# First argument is the name of the blueprint folder
# Second is always __name__ attribute
# Third parameter tells what folder contains your templates
# 4th is url prefix which makes routers cleaner
ud = Blueprint('ud',__name__,template_folder='templates',url_prefix=('/app/'))

# /app/delete
@ud.route('delete/<int:id>')
def delete(id):
    return "Delete " + str(id)

@ud.route('update')
def update():
    return "Update"

@ud.route('addfriend',methods=['GET','POST'])
def addfriend():
    newfriend = FriendForm()
        # Check if get method
    if request.method == 'GET':
        return render_template('addfriend.html',form=newfriend,isLogged=True)
    else:
        if newfriend.validate_on_submit():
            # first solution below without db.relationship 
            friends = Friends(newfriend.name.data, newfriend.address.data, newfriend.age.data, session['user_id'])
            if newfriend.upload_file.data:
                #save the image if present
                filename = secure_filename(newfriend.upload_file.data.filename)
                newfriend.upload_file.data.save('app/static/images/' + newfriend.upload_file.data.filename)
                friends.filename = '/static/images/' + filename
            # second solution with db.relationship
            # friend = Users.query.get(session['user_id'])
            # print(friend.friends)            
            db.session.add(friends)
            db.session.commit()
            flash('New friend, {0} added to list!'.format(newfriend.name.data))            
            user = Users.query.get(session['user_id'])
            return render_template('friends.html',isLogged=True,friends=user.friends)
        else:
            flash('Check fields!')
            return render_template('addfriend.html',form=newfriend,isLogged=True)


def before_request():
    if not 'isLogged' in session:
        return redirect('/')
    
ud.before_request(before_request)