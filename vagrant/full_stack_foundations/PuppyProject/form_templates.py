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

class CreatePuppyForm(Form):
    name = TextField('Name', [validators.Length(min=2, max=25)])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')])
    birthday = DateTimeField('Date of birth', format='%m/%d/%y')
    shelter_id = IntegerField('Shelter ID')
    weight = DecimalField('Weight', places=2, rounding=None)

class CreateShelterForm(Form):
    name = TextField('Name', [validators.Length(min=2, max=25)])
    address = TextAreaField('Address', [validators.length(max=200)])
    city = TextField('City', [validators.Length(min=2, max=40)])
    state = TextField('State', [validators.Length(min=2, max=40)])
    zipCode = TextField('Zip Code', [validators.Length(min=2, max=25)])
    website = TextField ('Website')
    maximum_capacity = IntegerField('Maximum Capacity')
