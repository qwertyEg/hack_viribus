from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app.models.material import Material
from app.models.rating import Rating
from app.models.category import Category
from app import db
from app.forms.upload_form import UploadForm
from app.forms.rating_form import RatingForm
from app.services.drive_service import DriveService
from werkzeug.utils import secure_filename
from sqlalchemy import or_
import os

bp = Blueprint('material', __name__)

@bp.route('/')
def index():
    return redirect(url_for('material.list'))

@bp.route('/materials')
def list():
    page = request.args.get('page', 1, type=int)
    query = request.args.get('query', '')
    category_id = request.args.get('category_id', type=int)
    min_rating = request.args.get('min_rating', type=float)
    
    materials_query = Material.query.filter_by(status='approved')
    
    if query:
        materials_query = materials_query.filter(
            or_(
                Material.title.ilike(f'%{query}%'),
                Material.description.ilike(f'%{query}%')
            )
        )
    
    if category_id:
        materials_query = materials_query.filter_by(category_id=category_id)
    
    if min_rating is not None:
        materials_query = materials_query.filter(Material.average_rating_value >= min_rating)
    
    materials = materials_query.paginate(page=page, per_page=9)
    categories = Category.query.all()
    
    return render_template('materials/list.html', materials=materials, categories=categories, min_rating=min_rating)

@bp.route('/materials/<int:id>')
def detail(id):
    material = Material.query.get_or_404(id)
    form = RatingForm()
    return render_template('materials/detail.html', material=material, form=form)

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        if form.file.data:
            filename = secure_filename(form.file.data.filename)
            file_url = DriveService.upload_file(form.file.data)
            
            material = Material(
                title=form.title.data,
                description=form.description.data,
                file_url=file_url,
                author_id=current_user.id,
                category_id=form.category_id.data
            )
            
            db.session.add(material)
            db.session.commit()
            flash('Материал успешно загружен! Ожидайте модерации.', 'success')
            return redirect(url_for('material.list'))
    
    return render_template('materials/upload.html', form=form)

@bp.route('/materials/<int:id>/rate', methods=['POST'])
@login_required
def rate(id):
    form = RatingForm()
    if form.validate_on_submit():
        material = Material.query.get_or_404(id)
        
        # Проверяем, есть ли уже оценка от этого пользователя
        existing_rating = Rating.query.filter_by(
            user_id=current_user.id,
            material_id=material.id
        ).first()
        
        if existing_rating:
            # Обновляем существующую оценку
            existing_rating.value = form.rating_value.data
            flash('Ваша оценка обновлена.', 'success')
        else:
            # Создаем новую оценку
            rating = Rating(
                value=form.rating_value.data,
                user_id=current_user.id,
                material_id=material.id
            )
            db.session.add(rating)
            flash('Спасибо за вашу оценку!', 'success')
        
        # Сохраняем изменения в базе данных
        db.session.commit()
        
        # Обновляем среднюю оценку материала
        material.update_average_rating()
        db.session.commit()
    else:
        flash('Пожалуйста, выберите оценку от 1 до 5.', 'error')
    
    return redirect(url_for('material.detail', id=id)) 