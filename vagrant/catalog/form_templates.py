# Import the required wtform module and associated classes.
from wtforms import Form, BooleanField, DecimalField, IntegerField, TextField, TextAreaField, PasswordField, validators, SelectField, DateTimeField


# Create a registration form class with required fields. 
class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.Required()])

class CreateCategoryItemForm(Form):
    name = TextField('Name', [validators.Length(min=2, max=40)])
    description = TextField('Description', [validators.length(max=200)])
    price = DecimalField('Weight', places=2, rounding=None)
    picture = TextField('Picture URL')

class CreateCategoryForm(Form):
    name = TextField('Name', [validators.Length(min=2, max=40)])
