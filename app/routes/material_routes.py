from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_file, Response
from flask_login import login_required, current_user
from app.models.material import Material
from app.models.rating import Rating
from app.models.category import Category
from app import db
from app.forms.upload_form import UploadForm
from app.forms.rating_form import RatingForm
from app.services.cloudinary_service import CloudinaryService
from werkzeug.utils import secure_filename
import os
import requests
from io import BytesIO

bp = Blueprint('material', __name__)

@bp.route('/')
def index():
    return redirect(url_for('material.list'))

@bp.route('/materials')
@login_required
def list():
    # Получаем параметры фильтрации
    category_id = request.args.get('category_id', type=int)
    min_rating = request.args.get('min_rating', type=float)
    
    # Базовый запрос
    query = Material.query
    
    # Фильтр по категории
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # Фильтр по рейтингу
    if min_rating:
        query = query.filter(Material.rating_sum / Material.rating_count >= min_rating)
    
    # Получаем материалы
    materials = query.all()
    
    # Получаем список всех категорий для фильтра
    categories = Category.query.all()
    
    return render_template('material/list.html', 
                         materials=materials,
                         categories=categories,
                         selected_category_id=category_id,
                         min_rating=min_rating)

@bp.route('/<int:material_id>')
@login_required
def view(material_id):
    material = Material.query.get_or_404(material_id)
    cloudinary_service = CloudinaryService()
    form = RatingForm()
    return render_template('material/view.html', material=material, cloudinary_service=cloudinary_service, form=form)

@bp.route('/materials/<int:material_id>/preview')
@login_required
def preview(material_id):
    material = Material.query.get_or_404(material_id)
    cloudinary_service = CloudinaryService()
    
    try:
        if material.file_id.endswith('.mp4'):
            # Для видео показываем через плеер
            return redirect(url_for('material.view', material_id=material_id))
        else:
            # Для документов показываем через сервер
            file_content = cloudinary_service.get_file_content(material.file_id)
            return send_file(
                file_content,
                mimetype='application/pdf',
                as_attachment=False
            )
    except Exception as e:
        flash(f'Ошибка при просмотре файла: {str(e)}')
        return redirect(url_for('material.view', material_id=material_id))

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    print("Upload route called")
    form = UploadForm()
    print(f"Form created. Method: {request.method}")
    
    if request.method == 'POST':
        print("POST request received")
        print(f"Form data: {request.form}")
        print(f"Files: {request.files}")
        
        if form.validate_on_submit():
            print("Form validated successfully")
            print(f"Material type: {form.material_type.data}")
            print(f"File data: {form.file.data}")
            print(f"Video URL: {form.video_url.data}")
            
            try:
                # Обработка категории
                if form.create_new_category.data:
                    print("Creating new category")
                    # Создаем новую категорию
                    category = Category(name=form.new_category.data)
                    db.session.add(category)
                    db.session.commit()
                    category_id = category.id
                else:
                    category_id = form.category_id.data
                    print(f"Using existing category: {category_id}")

                if form.material_type.data == 'file':
                    print("Processing file upload")
                    # Обработка загрузки файла
                    file = form.file.data
                    if file:
                        print(f"File received: {file.filename}")
                        filename = secure_filename(file.filename)
                        upload_folder = current_app.config['UPLOAD_FOLDER']
                        os.makedirs(upload_folder, exist_ok=True)
                        file_path = os.path.join(upload_folder, filename)
                        file.save(file_path)

                        # Загрузка в Cloudinary
                        cloudinary = CloudinaryService()
                        result = cloudinary.upload_file(file_path, folder_name=str(category_id))
                        os.remove(file_path)  # Удаляем временный файл

                        # Создаем запись о материале
                        material = Material(
                            title=form.title.data,
                            description=form.description.data,
                            file_id=result['public_id'],
                            user_id=current_user.id,
                            category_id=category_id,
                            status='unapproved'
                        )
                else:
                    print("Processing video URL")
                    # Обработка видео URL
                    material = Material(
                        title=form.title.data,
                        description=form.description.data,
                        video_url=form.video_url.data,
                        user_id=current_user.id,
                        category_id=category_id,
                        status='unapproved'
                    )

                db.session.add(material)
                db.session.commit()
                print("Material saved to database")
                flash('Материал успешно загружен и ожидает модерации', 'success')
                return redirect(url_for('material.list'))

            except Exception as e:
                print(f"Error during upload: {str(e)}")
                flash(f'Ошибка при загрузке материала: {str(e)}', 'error')
                db.session.rollback()
        else:
            print("Form validation failed")
            print(f"Form errors: {form.errors}")
            for field, errors in form.errors.items():
                print(f"Field {field} errors: {errors}")
        
    categories = Category.query.all()
    return render_template('material/upload.html', form=form, categories=categories)

@bp.route('/materials/<int:material_id>/download')
@login_required
def download(material_id):
    material = Material.query.get_or_404(material_id)
    cloudinary_service = CloudinaryService()
    
    try:
        file_content = cloudinary_service.get_file_content(material.file_id)
        
        # Определяем MIME-тип в зависимости от расширения файла
        if material.file_id.endswith('.mp4'):
            mimetype = 'video/mp4'
            extension = 'mp4'
        else:
            mimetype = 'application/pdf'
            extension = 'pdf'
        
        return send_file(
            file_content,
            as_attachment=True,
            download_name=f"{material.title}.{extension}",
            mimetype=mimetype
        )
    except Exception as e:
        flash(f'Ошибка при скачивании файла: {str(e)}')
        return redirect(url_for('material.view', material_id=material_id))

@bp.route('/materials/<int:material_id>/rate', methods=['POST'])
@login_required
def rate(material_id):
    form = RatingForm()
    if form.validate_on_submit():
        material = Material.query.get_or_404(material_id)
        rating = Rating.query.filter_by(
            user_id=current_user.id,
            material_id=material.id
        ).first()
        
        if rating:
            rating.value = form.rating.data
        else:
            rating = Rating(
                user_id=current_user.id,
                material_id=material.id,
                value=form.rating.data
            )
            db.session.add(rating)
        
        db.session.commit()
        flash('Ваша оценка сохранена')
    
    return redirect(url_for('material.view', material_id=material_id)) 