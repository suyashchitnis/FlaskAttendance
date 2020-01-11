from flask_wtf import FlaskForm
from flaskblog.models import Stud
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileRequired,FileAllowed,FileField,FileStorage
from wtforms import StringField, PasswordField, SubmitField, BooleanField,IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User 
import datetime

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class StudentStoreForm(FlaskForm):
    Id = IntegerField('ID')
    sname = StringField('Student_name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    sdob = DateField('DOB',validators=[DataRequired()])
    saddress= StringField('Address', validators=[DataRequired()])
    slandmark = StringField("Landmark")
    saddmission = DateField("Joining Date",default=datetime.date.today())
    file = FileField('File',validators=[FileRequired()])
    submit = SubmitField('Submit')