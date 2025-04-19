from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.material import Material
from app import db

bp = Blueprint('moderation', __name__)

@bp.route('/moderation')
@login_required
def panel():
    if not current_user.is_moderator():
        flash('У вас нет прав для доступа к этой странице.', 'danger')
        return redirect(url_for('material.list'))
    
    materials = Material.query.filter_by(status='unapproved').all()
    return render_template('moderation/panel.html', materials=materials)

@bp.route('/moderation/approve/<int:id>')
@login_required
def approve(id):
    if not current_user.is_moderator():
        flash('У вас нет прав для выполнения этого действия.', 'danger')
        return redirect(url_for('material.list'))
    
    material = Material.query.get_or_404(id)
    material.approve()
    flash('Материал одобрен.', 'success')
    return redirect(url_for('moderation.panel'))

@bp.route('/moderation/reject/<int:id>')
@login_required
def reject(id):
    if not current_user.is_moderator():
        flash('У вас нет прав для выполнения этого действия.', 'danger')
        return redirect(url_for('material.list'))
    
    material = Material.query.get_or_404(id)
    material.reject()
    flash('Материал отклонен.', 'success')
    return redirect(url_for('moderation.panel')) 