from flask_login import UserMixin
from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(UserMixin, db.Model):
    """User model for storing user account information"""
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    saved_cities = db.relationship('SavedCity', backref='user', lazy=True, 
                                 cascade='all, delete-orphan')

class SavedCity(db.Model):
    """Model for storing user's saved cities"""
    __tablename__ = 'saved_cities'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    city_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), 
                       nullable=False)
    added_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    
    # Add index for faster queries
    __table_args__ = (db.Index('idx_user_city', user_id, city_name),)
