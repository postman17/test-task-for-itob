from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SelectField,
    TextAreaField,
    DecimalField,
    validators
)
from app import Occupation


class LoginForm(FlaskForm):
    """Login form."""

    email = StringField('Email: ', validators=[validators.Email()])
    password = PasswordField('Password: ', [validators.DataRequired(), validators.Length(min=4, max=10)])


class RegistrationForm(FlaskForm):
    """Registration form."""

    email = StringField('Email: ', validators=[validators.Email()])
    password = PasswordField('Password: ', [validators.DataRequired(), validators.Length(min=4, max=20)])
    occupation = SelectField(u'Occupation: ', choices=[(occ.id, occ.name) for occ in Occupation.query.all()], coerce=int)


class ConsignorTaskForm(FlaskForm):
    """Consignor task form."""

    comment = TextAreaField('Comment: ', validators=[validators.DataRequired()])
    price = DecimalField('Price: ', places=2, validators=[validators.DataRequired()])
