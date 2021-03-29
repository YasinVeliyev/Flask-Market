from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from market.models import User

class RegisterForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(),Length(min=4,max=30)])
    email = StringField('Email Address', validators = [DataRequired(), Email()])
    password = PasswordField('Password', 
        validators = [DataRequired(),Length(min=6,max=14)])
    confirm_password = PasswordField('Repeat Password', validators = [DataRequired(),EqualTo('password',message = "Field must be equal to Password")])
    submit = SubmitField('Create Account')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
    

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Login')

class PurchaseForm(FlaskForm):
    submit = SubmitField('Buy')

class SellForm(FlaskForm):
    submit = SubmitField('Sell')