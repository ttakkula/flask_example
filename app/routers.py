from app import app
#render_template gives you access to Jinja2 template engine
from flask import render_template, request, make_response
@app.route('/')

def index():
    name = 'My Name'
    address = 'My address'
    # return render_template('template_index.html',title=address,name=name)
    response = make_response(render_template('template_index.html',title=address,name=name))
    response.headers.add('Content-Language','en')
    return response

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