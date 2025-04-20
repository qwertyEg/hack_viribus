from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired, NumberRange

class RatingForm(FlaskForm):
    rating = IntegerField('Оценка', validators=[
        DataRequired(),
        NumberRange(min=1, max=5, message='Оценка должна быть от 1 до 5')
    ]) 