from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField , PasswordField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from wtforms.validators import DataRequired, Email, Regexp

class forgotPasswordForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )


    submit = SubmitField("Submit")

class codeForm(FlaskForm):
    code = StringField(
        "Code",
        validators=[DataRequired()]
    )

    submit = SubmitField("Submit")

class resetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=8, max=30), 
        Regexp(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
            message="Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character."
        )
    ])

    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[
            DataRequired(),
            EqualTo('password', message="Passwords must match.")
        ]
    )

    submit = SubmitField("Reset Password")