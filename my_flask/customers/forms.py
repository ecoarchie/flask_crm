from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length, Email


class CustomerForm(FlaskForm):
    first_name = StringField(
        label="First name", validators=[DataRequired(), Length(min=3, max=20)]
    )
    last_name = StringField(
        label="Last name", validators=[DataRequired(), Length(min=3, max=20)]
    )
    status = StringField(
        label="Status", validators=[DataRequired(), Length(min=3, max=20)]
    )
    company = StringField(
        label="Company", validators=[DataRequired(), Length(min=3, max=20)]
    )
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    submit = SubmitField(label="")


class CustomerNoteForm(FlaskForm):
    note_text = TextAreaField(label="Note text", validators=[DataRequired()])
    note_type = StringField(label="Note type")
    submit = SubmitField(label="")
