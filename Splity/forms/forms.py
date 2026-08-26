from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, SelectMultipleField, RadioField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange
from wtforms.widgets import CheckboxInput, ListWidget

class LoginForm(FlaskForm):
    username=StringField("Username", validators=[DataRequired()])
    password=PasswordField("Password", validators=[DataRequired()])
    submit=SubmitField("Sign In")

class RegistrationForm(FlaskForm):
    name=StringField("First and last name", validators=[DataRequired(), Length(min=2,max=100)])
    username=StringField("Username", validators=[DataRequired()])
    email=StringField("Email", validators=[DataRequired(),Email()])
    password=PasswordField("Password", validators=[DataRequired()])
    password2=PasswordField("Confirm Password", validators=[DataRequired(),EqualTo("password",message="Passwords must match.")])
    submit=SubmitField("Register")

class GroupCreationForm(FlaskForm):
    name=StringField("Group Name", validators=[DataRequired(),Length(min=2,max=50)])
    description=TextAreaField("Description", validators=[DataRequired()])
    currency=SelectField("Currency",choices=[],validators=[DataRequired()])
    submit=SubmitField("Create Group")

class GroupEditForm(FlaskForm):
    name=StringField("New Name",validators=[DataRequired(),Length(min=2,max=50)])
    description=TextAreaField("New Description",validators=[DataRequired()])
    submit=SubmitField("Change Details")

class JoinGroupForm(FlaskForm):
    invite_code=StringField("Invite Code",validators=[DataRequired(),Length(min=6,max=6)])
    submit=SubmitField("Join Group")

class SelectMultipleCheckboxesField(SelectMultipleField):
    widget=ListWidget(prefix_label=False)
    option_widget=CheckboxInput()

class CreateBillForm(FlaskForm):
    description=StringField("Description",validators=[DataRequired(),Length(min=2,max=50)])
    payer_id=SelectField("Paid by",coerce=int,validators=[DataRequired()])
    split_mode=RadioField("Split method",choices=[("equal","Split equally"),("custom","Custom amounts")],default="equal",validators=[DataRequired()])
    names=SelectMultipleCheckboxesField("Who shares this expense?",choices=[],coerce=int,validators=[DataRequired()])
    amount=DecimalField("Amount",validators=[DataRequired(),NumberRange(min=0.01)])
    submit=SubmitField("Save Expense")

class RepaymentForm(FlaskForm):
    payee_id=SelectField("Paid to",coerce=int,validators=[DataRequired()])
    amount=DecimalField("Amount",validators=[DataRequired(),NumberRange(min=0.01)])
    submit=SubmitField("I have paid")
