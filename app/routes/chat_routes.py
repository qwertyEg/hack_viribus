from flask import Blueprint, render_template

bp = Blueprint('chat', __name__)

@bp.route('/chat')
def index():
    return render_template('chat/index.html') 