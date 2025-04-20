from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, RadioField, BooleanField
from wtforms.validators import DataRequired, Length, URL, Optional, InputRequired, ValidationError
from app.models.category import Category

class UploadForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(max=120)])
    description = TextAreaField('Описание', validators=[DataRequired()])
    category_id = SelectField('Категория', coerce=int)
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
        print("Initializing UploadForm")
        categories = Category.query.order_by(Category.name).all()
        if categories:
            self.category_id.choices = [(c.id, c.name) for c in categories]
            print(f"Category choices: {self.category_id.choices}")
        else:
            print("No categories found")
            self.create_new_category.data = True
    
    def validate(self, extra_validators=None):
        print("Validating form")
        print(f"Form data: {self.data}")
        
        if not super().validate(extra_validators=extra_validators):
            print("Base validation failed")
            print(f"Errors: {self.errors}")
            return False
            
        if self.create_new_category.data and not self.new_category.data:
            print("New category validation failed")
            self.new_category.errors.append('Укажите название новой категории')
            return False
            
        if not self.create_new_category.data and not self.category_id.data:
            print("Category validation failed")
            self.category_id.errors.append('Выберите категорию')
            return False
            
        # Проверяем, что выбран хотя бы один тип материала
        if self.material_type.data == 'file' and not self.file.data:
            print("File validation failed")
            self.file.errors.append('Выберите файл для загрузки')
            return False
        elif self.material_type.data == 'video' and not self.video_url.data:
            print("Video URL validation failed")
            self.video_url.errors.append('Укажите ссылку на видео')
            return False
            
        print("Form validation successful")
        return True 