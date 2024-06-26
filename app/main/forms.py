from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Email,EqualTo,ValidationError,Length
from app.models import User

class EditForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    about_me=TextAreaField('About me',validators=[Length(min=0,max=140)])
    submit=SubmitField('Submit')
    
    def __init__(self,original_username ,*args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        
    def validate_username(self,username):
        if username.data!=self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')
            

class EmptyForm(FlaskForm):
    submit=SubmitField()
    
class PostForm(FlaskForm):
    post=TextAreaField('Say something',validators=[DataRequired(),Length(min=10,max=140)])
    submit=SubmitField('Submit')