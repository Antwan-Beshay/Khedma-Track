from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField , BooleanField , SelectField
from wtforms.validators import DataRequired, Length, Regexp, Email, EqualTo

class registerForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=30)])
    lname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=30)])
    uname = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    
    email = StringField('Email', validators=[DataRequired(), Email()]) 
    
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=8, max=30), 
        Regexp(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
            message="Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character."
        )
    ])
    
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    role = SelectField(
        "Account Type",
        choices=[
            ("student", "Student"),
            ("teacher", "Teacher")
        ]
    )

    submit = SubmitField('Sign Up')

class loginform(FlaskForm):
    mail = StringField('Email', validators=[DataRequired(), Email()]) 
    password = PasswordField('Password', validators=[
        DataRequired()])
    remmeber = BooleanField("Remember Me")
    submit = SubmitField('Login')
    
    