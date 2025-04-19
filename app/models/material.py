from datetime import datetime
from app import db

class Material(db.Model):
    __tablename__ = 'materials'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    file_url = db.Column(db.String(500))  # Ссылка на Google Drive
    status = db.Column(db.String(20), default='unapproved')  # unapproved/approved/rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    ratings = db.relationship('Rating', backref='material', lazy='dynamic')

    def average_rating(self):
        ratings = self.ratings.all()
        if not ratings:
            return 0
        return sum(rating.value for rating in ratings) / len(ratings)

    def is_approved(self):
        return self.status == 'approved'

    def approve(self):
        self.status = 'approved'
        db.session.commit()

    def reject(self):
        self.status = 'rejected'
        db.session.commit() 