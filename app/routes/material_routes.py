from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app.models.material import Material
from app.models.rating import Rating
from app import db
from app.forms.upload_form import UploadForm
from app.forms.rating_form import RatingForm
from app.services.drive_service import DriveService
from werkzeug.utils import secure_filename
import os

bp = Blueprint('material', __name__)

@bp.route('/')
def index():
    return redirect(url_for('material.list'))

@bp.route('/materials')
def list():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category_id', type=int)
    query = Material.query.filter_by(status='approved')
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    materials = query.paginate(page=page, per_page=10)
    return render_template('materials/list.html', materials=materials)

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
        rating = Rating.query.filter_by(
            user_id=current_user.id,
            material_id=material.id
        ).first()
        
        if rating:
            rating.value = form.rating_value.data
        else:
            rating = Rating(
                value=form.rating_value.data,
                user_id=current_user.id,
                material_id=material.id
            )
            db.session.add(rating)
        
        db.session.commit()
        flash('Ваша оценка сохранена.', 'success')
    
    return redirect(url_for('material.detail', id=id)) 