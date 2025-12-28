# /Splity_flask/Splity/forms/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password',
                              validators=[DataRequired(),
                                          EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')


class GroupCreationForm(FlaskForm):
    name = StringField('Group Name', validators=[DataRequired(), Length(min=2, max=50)])
    description = TextAreaField('Description', validators=[DataRequired()])
    currency = SelectField('Currency', choices=[], validators=[DataRequired()])
    submit = SubmitField('Create Group')


class GroupEditForm(FlaskForm):
    name = StringField('New Name', validators=[DataRequired(), Length(min=2, max=50)])
    description = TextAreaField('New Description', validators=[DataRequired()])
    submit = SubmitField('Change Details')


class JoinGroupForm(FlaskForm):
    invite_code = StringField('Invite Code', validators=[DataRequired(), Length(min=1, max=10)])
    submit = SubmitField('Join Group')


class CreateBillForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired(), Length(min=2, max=50)])
    owe_members = SelectMultipleField('Owe Member', choices=[], validators=[DataRequired()])
    submit = SubmitField('Create Bill')