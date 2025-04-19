from datetime import datetime
from app import db

class Material(db.Model):
    __tablename__ = 'materials'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    file_id = db.Column(db.String(100), nullable=False)  # ID файла в Google Drive
    folder_id = db.Column(db.String(100))  # ID папки в Google Drive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='unapproved')  # unapproved/approved/rejected
    ratings = db.relationship('Rating', backref='material', lazy='dynamic')

    # Связи
    user = db.relationship('User', overlaps="author,materials")
    category = db.relationship('Category', back_populates='materials')

    def __repr__(self):
        return f'<Material {self.title}>'

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