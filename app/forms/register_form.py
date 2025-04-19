from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp
from app.models.user import User
import re

class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[
        DataRequired(), 
        Length(min=3, max=64),
        Regexp(r'^[a-zA-Z0-9]+$', message='Имя пользователя может содержать только английские буквы и цифры')
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=8, message='Пароль должен содержать минимум 8 символов'),
        Regexp(
            r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$',
            message='Пароль должен содержать буквы, цифры и специальные символы'
        )
    ])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Это имя пользователя уже занято.')
            
    def validate_password(self, password):
        if not re.search(r'[A-Za-z]', password.data):
            raise ValidationError('Пароль должен содержать хотя бы одну букву')
        if not re.search(r'\d', password.data):
            raise ValidationError('Пароль должен содержать хотя бы одну цифру')
        if not re.search(r'[@$!%*#?&]', password.data):
            raise ValidationError('Пароль должен содержать хотя бы один специальный символ') 