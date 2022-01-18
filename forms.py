from mymovielist import STATUSES
from service.crud import check_username
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo, ValidationError


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        if check_username(username.data):
            raise ValidationError('This username is already taken')


class EntryForm(FlaskForm):
    status = SelectField('Status', choices=[('', 'Select')] + [(status, status) for status in STATUSES])
    score = SelectField('Score', choices=[('', 'Select')] + [(count, count) for count in range(1, 11)])