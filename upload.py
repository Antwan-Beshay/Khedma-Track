from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class postform(FlaskForm):
    Title = StringField(
        "Title",
        validators=[DataRequired(), Length(min=10, max=50)]
    )

    content = StringField(
        "Content",
        validators=[DataRequired(), Length(min=20, max=500)]
    )

    image = FileField(
        "Image",
        validators=[FileRequired()]
    )

    submit = SubmitField("Publish")
    