from flask import Blueprint, render_template, request
from app.models.material import Material
from app.models.category import Category
from sqlalchemy import or_

bp = Blueprint('search', __name__)

@bp.route('/search')
def search():
    query = request.args.get('query', '')
    category_id = request.args.get('category_id', type=int)
    page = request.args.get('page', 1, type=int)
    
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
    
    materials = materials_query.paginate(page=page, per_page=10)
    categories = Category.query.all()
    
    return render_template('materials/search.html',
                         materials=materials,
                         categories=categories,
                         query=query,
                         selected_category=category_id) 