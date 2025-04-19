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
    # Получаем ID категории из параметров запроса
    category_id = request.args.get('category_id', type=int)
    
    # Если указана категория, фильтруем материалы
    if category_id:
        materials = Material.query.filter_by(category_id=category_id).all()
    else:
        # Иначе показываем все материалы
        materials = Material.query.all()
    
    # Получаем список всех категорий для фильтра
    categories = Category.query.all()
    
    return render_template('material/list.html', 
                         materials=materials,
                         categories=categories,
                         selected_category_id=category_id)

@bp.route('/materials/<int:id>')
@login_required
def view(id):
    material = Material.query.get_or_404(id)
    return render_template('material/view.html', 
                         material=material)

@bp.route('/materials/<int:id>/preview')
@login_required
def preview(id):
    material = Material.query.get_or_404(id)
    cloudinary_service = CloudinaryService()
    
    try:
        file_content = cloudinary_service.get_file_content(material.file_id)
        return send_file(
            file_content,
            mimetype='application/pdf',
            as_attachment=False
        )
    except Exception as e:
        flash(f'Ошибка при просмотре файла: {str(e)}')
        return redirect(url_for('material.view', id=id))

@bp.route('/materials/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        if 'file' not in request.files:
            flash('Файл не выбран')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('Файл не выбран')
            return redirect(request.url)
        
        if file:
            try:
                # Создаем директорию для загрузки, если она не существует
                os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
                
                # Генерируем безопасное имя файла
                filename = secure_filename(file.filename)
                temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                
                # Сохраняем файл
                file.save(temp_path)
                
                # Загружаем файл в Cloudinary
                cloudinary_service = CloudinaryService()
                result = cloudinary_service.upload_file(temp_path, current_user.username)
                
                # Создаем запись в базе данных
                material = Material(
                    title=form.title.data,
                    description=form.description.data,
                    file_id=result['public_id'],
                    user_id=current_user.id,
                    category_id=form.category_id.data,
                    status='approved'  # Устанавливаем статус одобрен сразу
                )
                db.session.add(material)
                db.session.commit()
                
                # Удаляем временный файл
                os.remove(temp_path)
                
                flash('Материал успешно загружен')
                return redirect(url_for('material.list'))
            except Exception as e:
                flash(f'Ошибка при загрузке: {str(e)}')
                return redirect(request.url)
    
    return render_template('material/upload.html', form=form)

@bp.route('/materials/<int:id>/download')
@login_required
def download(id):
    material = Material.query.get_or_404(id)
    cloudinary_service = CloudinaryService()
    
    try:
        file_content = cloudinary_service.get_file_content(material.file_id)
        return send_file(
            file_content,
            as_attachment=True,
            download_name=f"{material.title}.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        flash(f'Ошибка при скачивании файла: {str(e)}')
        return redirect(url_for('material.view', id=id))

@bp.route('/materials/<int:id>/rate', methods=['POST'])
@login_required
def rate(id):
    form = RatingForm()
    if form.validate_on_submit():
        material = Material.query.get_or_404(id)
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
    
    return redirect(url_for('material.view', id=id)) 