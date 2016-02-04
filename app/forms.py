from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, PasswordField, SubmitField, FileField
from wtforms.validators import Required, Email, NumberRange

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
    age = IntegerField('Enter friends age', validators=[Required(),NumberRange(min=0,max=120,message="Enter value between 0-120")])
    upload_file = FileField('Upload image')
    submit = SubmitField('Add friend')
    
