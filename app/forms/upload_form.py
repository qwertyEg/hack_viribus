from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, RadioField, BooleanField
from wtforms.validators import DataRequired, Length, URL, Optional, InputRequired, ValidationError
from app.models.category import Category

class UploadForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(max=120)])
    description = TextAreaField('Описание', validators=[DataRequired()])
    category_id = SelectField('Категория', coerce=int, validators=[DataRequired()])
    new_category = StringField('Новая категория', validators=[Optional()])
    create_new_category = BooleanField('Создать новую категорию')
    
    # Выбор типа материала
    material_type = RadioField('Тип материала', 
                             choices=[('file', 'Файл'), ('video', 'Видео')],
                             validators=[InputRequired()],
                             default='file')
    
    # Поля для файла
    file = FileField('Файл', validators=[
        Optional(),
        FileAllowed(['pdf', 'doc', 'docx', 'txt', 'ppt', 'pptx'], 'Допустимые форматы: PDF, DOC, DOCX, TXT, PPT, PPTX')
    ])
    
    # Поле для видео URL
    video_url = StringField('URL видео', validators=[
        Optional(),
        URL(message='Введите корректный URL видео')
    ])
    
    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
    
    def validate(self, extra_validators=None):
        if not super().validate(extra_validators=extra_validators):
            return False
            
        if self.create_new_category.data and not self.new_category.data:
            self.new_category.errors.append('Укажите название новой категории')
            return False
            
        # Проверяем, что выбран хотя бы один тип материала
        if self.material_type.data == 'file' and not self.file.data:
            self.file.errors.append('Выберите файл для загрузки')
            return False
        elif self.material_type.data == 'video' and not self.video_url.data:
            self.video_url.errors.append('Укажите ссылку на видео')
            return False
            
        return True 