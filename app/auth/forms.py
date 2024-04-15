from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Email,EqualTo,ValidationError,Length
from app.models import User

class LoginForm(FlaskForm):
    username=StringField(_l('Username'),validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember_me=BooleanField('Remember me')
    submit=SubmitField('Sign in')
    

class RegisterForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    password2=PasswordField('Password2',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Register')
    
    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username')
        
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email')
        

            

    
class ResetPasswordRequestForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    submit=SubmitField('Request password reset')
    
class ResetPasswordForm(FlaskForm):
    password=PasswordField('Password',validators=[DataRequired()])
    password2=PasswordField('Reset password',validators=[DataRequired(),EqualTo('Password')])
    submit=SubmitField('Request password Reset')


    