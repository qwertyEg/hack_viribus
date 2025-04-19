from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length
from app.models.category import Category

class UploadForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(max=120)])
    description = TextAreaField('Описание', validators=[DataRequired()])
    category_id = SelectField('Категория', coerce=int)
    file = FileField('Файл', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'doc', 'docx', 'txt', 'ppt', 'pptx'], 'Только документы!')
    ])
    
    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(c.id, c.name) for c in Category.query.all()] 