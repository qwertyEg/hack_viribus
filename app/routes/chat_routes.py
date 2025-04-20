from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('chat', __name__)

@bp.route('/chat')
@login_required
def chat():
    return render_template('chat/chat.html') 