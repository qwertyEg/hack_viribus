from datetime import datetime
from app import db
from app.models.rating import Rating

class Material(db.Model):
    __tablename__ = 'materials'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    file_id = db.Column(db.String(255), nullable=True)
    video_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    status = db.Column(db.String(20), default='unapproved')
    ratings = db.relationship('Rating', backref='material', lazy=True)
    rating_sum = db.Column(db.Integer, default=0)  # Сумма всех оценок
    rating_count = db.Column(db.Integer, default=0)  # Количество оценок

    user = db.relationship('User', overlaps="author,materials")
    category = db.relationship('Category', back_populates='materials')

    def __repr__(self):
        return f'<Material {self.title}>'

    def average_rating(self):
        if not self.rating_count or not self.rating_sum or self.rating_count == 0:
            return 0
        return round(self.rating_sum / self.rating_count, 1)

    def add_rating(self, value):
        """Добавляет новую оценку и обновляет среднее значение"""
        self.rating_sum = (self.rating_sum or 0) + value
        self.rating_count = (self.rating_count or 0) + 1
        db.session.commit()

    def update_rating(self, old_value, new_value):
        """Обновляет существующую оценку"""
        self.rating_sum = (self.rating_sum or 0) - old_value + new_value
        db.session.commit()

    def remove_rating(self, value):
        """Удаляет оценку"""
        self.rating_sum = (self.rating_sum or 0) - value
        self.rating_count = (self.rating_count or 0) - 1
        if self.rating_count < 0:
            self.rating_count = 0
        if self.rating_sum < 0:
            self.rating_sum = 0
        db.session.commit()

    def get_user_rating(self, user_id):
        """Получает оценку пользователя для материала"""
        rating = Rating.query.filter_by(
            user_id=user_id,
            material_id=self.id
        ).first()
        return rating.value if rating else 0

    def is_approved(self):
        return self.status == 'approved'

    def approve(self):
        self.status = 'approved'
        db.session.commit()

    def reject(self):
        self.status = 'rejected'
        db.session.commit()

    def get_embed_url(self):
        if not self.video_url:
            return None
            
        if 'youtube.com' in self.video_url or 'youtu.be' in self.video_url:
            if 'youtu.be' in self.video_url:
                video_id = self.video_url.split('/')[-1]
            else:
                video_id = self.video_url.split('v=')[1].split('&')[0]
            return f'https://www.youtube.com/embed/{video_id}'
            
        elif 'vimeo.com' in self.video_url:
            video_id = self.video_url.split('/')[-1]
            return f'https://player.vimeo.com/video/{video_id}'
            
        elif 'vk.com' in self.video_url:
            parts = self.video_url.split('video-')[1].split('_')
            owner_id = parts[0]
            video_id = parts[1]
            return f'https://vk.com/video_ext.php?oid={owner_id}&id={video_id}&hash='
            
        elif 'rutube.ru' in self.video_url:
            video_id = self.video_url.split('/')[-2]
            return f'https://rutube.ru/play/embed/{video_id}'
            
        elif 'mail.ru' in self.video_url and '/video/' in self.video_url:
            video_id = self.video_url.split('/')[-1]
            return f'https://my.mail.ru/video/embed/{video_id}'
            
        elif 'video.yandex.ru' in self.video_url:
            video_id = self.video_url.split('/')[-2]
            return f'https://video.yandex.ru/iframe/{video_id}'
            
        elif 'dailymotion.com' in self.video_url:
            video_id = self.video_url.split('/')[-1]
            return f'https://www.dailymotion.com/embed/video/{video_id}'
            
        return self.video_url 