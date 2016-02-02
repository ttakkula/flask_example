from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import Required, Email

class LoginForm(Form):
    email = StringField('Enter your email', validators=[Required(),Email()])
    passw = PasswordField('Enter password', validators=[Required()])
    submit = SubmitField('Login')

class RegisterForm(Form):
    email = StringField('Enter your email', validators=[Required(),Email()])
    passw = PasswordField('Enter password', validators=[Required()])
    submit = SubmitField('Register')
    
class FriendForm(Form):
    name = StringField('Enter friends name', validators=[Required()])
    address = StringField('Enter friends address', validators=[Required()])
    age = IntegerField('Enter friends age', validators=[Required()])
    submit = SubmitField('Add friend')    
