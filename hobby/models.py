from database import db
from datetime import datetime


class Idea(db.Model):
    """Модель для хранения идей хобби"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    time_required = db.Column(db.String(20), nullable=False)  # 'short', 'medium', 'long'
    budget = db.Column(db.String(20), nullable=False)  # 'free', 'low', 'medium', 'high'
    location = db.Column(db.String(20), nullable=False)  # 'indoor', 'outdoor', 'both'
    difficulty = db.Column(db.String(20), nullable=False)  # 'easy', 'medium', 'hard'
    votes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_approved = db.Column(db.Boolean, default=False)  # Для модерации идей от пользователей

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'time_required': self.time_required,
            'budget': self.budget,
            'location': self.location,
            'difficulty': self.difficulty,
            'votes': self.votes,
            'created_at': self.created_at.strftime('%d.%m.%Y')
        }


class DailyChallenge(db.Model):
    """Модель для ежедневных челленджей"""
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False)
    idea_id = db.Column(db.Integer, db.ForeignKey('idea.id'), nullable=False)
    completed_count = db.Column(db.Integer, default=0)

    # Связь с идеей
    idea = db.relationship('Idea', backref='daily_challenges')


class UserIdea(db.Model):
    """Модель для идей, добавленных пользователями"""
    id = db.Column(db.Integer, primary_key=True)
    idea_id = db.Column(db.Integer, db.ForeignKey('idea.id'), nullable=False)
    user_session = db.Column(db.String(100), nullable=False)  # Идентификатор сессии
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Связь с идеей
    idea = db.relationship('Idea', backref='user_ideas')