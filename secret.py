from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SecretKeyForm(FlaskForm):
    Secret_Key = StringField(
        "Secret_Key",
        validators=[DataRequired()]
    )


    submit = SubmitField("Submit")