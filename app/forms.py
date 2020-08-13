from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


class TaskForm(FlaskForm):
    task = TextAreaField('Add a todo item', validators=[DataRequired()])
    priority = RadioField('Priority', choices=[(1, 'High'), (2, 'Medium'), (3, 'Low')], default=1, coerce=int)
    status = BooleanField('Complete')
    submit = SubmitField('Submit')

class EmailForm(FlaskForm):
    email = StringField('Email To', validators=[DataRequired(), Email()])
    msg = TextAreaField('Add a message', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EmailForm2(FlaskForm):
    selfmail = BooleanField('Mail to self', default=1)
    msg = TextAreaField('Add a message', validators=[DataRequired()])
    submit = SubmitField('Submit')