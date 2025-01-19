# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask extensions
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # PostgreSQL Configuration
    app.config['SECRET_KEY'] = 1233
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/weather_app'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    bcrypt.init_app(app)
    
    # Register blueprints
    from auth import auth_bp
    from views import views_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(views_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

# models.py
# from flask_login import UserMixin
# from app import db
# from datetime import datetime
# from sqlalchemy.dialects.postgresql import UUID
# import uuid

# class User(UserMixin, db.Model):
#     """User model for storing user account information"""
#     __tablename__ = 'users'

#     id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password_hash = db.Column(db.String(128), nullable=False)
#     full_name = db.Column(db.String(100), nullable=False)
#     created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
#     saved_cities = db.relationship('SavedCity', backref='user', lazy=True, 
#                                  cascade='all, delete-orphan')

# class SavedCity(db.Model):
#     """Model for storing user's saved cities"""
#     __tablename__ = 'saved_cities'

#     id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     city_name = db.Column(db.String(100), nullable=False)
#     user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), 
#                        nullable=False)
#     added_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    
#     # Add index for faster queries
#     __table_args__ = (db.Index('idx_user_city', user_id, city_name),)

# auth.py
# from flask import Blueprint, request, jsonify, session
# from flask_login import login_user, logout_user, login_required, current_user
# from models import User, db
# from app import bcrypt
# from sqlalchemy.exc import IntegrityError

# auth_bp = Blueprint('auth', __name__)

# @auth_bp.route('/signup', methods=['POST'])
# def signup():
#     """Handle user registration"""
#     try:
#         data = request.form
        
#         # Check if user already exists
#         if User.query.filter_by(email=data['signup_email']).first():
#             return jsonify({'error': 'Email already registered'}), 400
        
#         # Create new user
#         hashed_password = bcrypt.generate_password_hash(data['signup_passwd']).decode('utf-8')
#         new_user = User(
#             email=data['signup_email'],
#             password_hash=hashed_password,
#             full_name=data['full_name']
#         )
        
#         db.session.add(new_user)
#         db.session.commit()
        
#         login_user(new_user)
#         return jsonify({'message': 'Registration successful'}), 201
        
#     except IntegrityError:
#         db.session.rollback()
#         return jsonify({'error': 'Database error occurred'}), 500
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500

# @auth_bp.route('/login', methods=['POST'])
# def login():
#     """Handle user login"""
#     try:
#         data = request.form
#         user = User.query.filter_by(email=data['login_email']).first()
        
#         if user and bcrypt.check_password_hash(user.password_hash, data['login_passwd']):
#             login_user(user)
#             return jsonify({'message': 'Login successful'}), 200
        
#         return jsonify({'error': 'Invalid credentials'}), 401
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @auth_bp.route('/logout')
# @login_required
# def logout():
#     """Handle user logout"""
#     logout_user()
#     return jsonify({'message': 'Logout successful'}), 200

# @auth_bp.route('/delete_account', methods=['DELETE'])
# @login_required
# def delete_account():
#     """Handle account deletion"""
#     try:
#         user = current_user
#         db.session.delete(user)
#         db.session.commit()
#         logout_user()
#         return jsonify({'message': 'Account deleted successfully'}), 200
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500

# views.py
# from flask import Blueprint, jsonify, request, render_template
# from flask_login import login_required, current_user
# from models import User, SavedCity, db
# from sqlalchemy.exc import IntegrityError

# views_bp = Blueprint('views', __name__)

# @views_bp.route('/')
# def index():
#     """Render main page"""
#     return render_template('main.html')

# @views_bp.route('/homepage')
# @login_required
# def homepage():
#     """Render homepage for logged-in users"""
#     return render_template('homepage.html')

# @views_bp.route('/update_profile', methods=['POST'])
# @login_required
# def update_profile():
#     """Update user profile information"""
#     try:
#         data = request.json
        
#         # Check if email is being changed and if it's already taken
#         if 'email' in data and data['email'] != current_user.email:
#             if User.query.filter_by(email=data['email']).first():
#                 return jsonify({'error': 'Email already in use'}), 400
        
#         current_user.full_name = data.get('username', current_user.full_name)
#         current_user.email = data.get('email', current_user.email)
        
#         db.session.commit()
#         return jsonify({'message': 'Profile updated successfully'}), 200
#     except IntegrityError:
#         db.session.rollback()
#         return jsonify({'error': 'Database error occurred'}), 500
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500

# @views_bp.route('/change_password', methods=['POST'])
# @login_required
# def change_password():
#     """Change user password"""
#     try:
#         data = request.json
        
#         if not bcrypt.check_password_hash(current_user.password_hash, data['current_password']):
#             return jsonify({'error': 'Current password is incorrect'}), 400
        
#         new_password_hash = bcrypt.generate_password_hash(data['new_password']).decode('utf-8')
#         current_user.password_hash = new_password_hash
#         db.session.commit()
        
#         return jsonify({'message': 'Password updated successfully'}), 200
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500

# @views_bp.route('/save_city', methods=['POST'])
# @login_required
# def save_city():
#     """Save a city to user's favorites"""
#     try:
#         data = request.json
        
#         # Check if city is already saved
#         existing_city = SavedCity.query.filter_by(
#             user_id=current_user.id,
#             city_name=data['city_name']
#         ).first()
        
#         if existing_city:
#             return jsonify({'error': 'City already saved'}), 400
        
#         new_city = SavedCity(
#             city_name=data['city_name'],
#             user_id=current_user.id
#         )
        
#         db.session.add(new_city)
#         db.session.commit()
        
#         return jsonify({'message': 'City saved successfully'}), 201
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500

# @views_bp.route('/get_saved_cities')
# @login_required
# def get_saved_cities():
#     """Get user's saved cities"""
#     try:
#         cities = SavedCity.query.filter_by(user_id=current_user.id).order_by(SavedCity.added_at.desc()).all()
#         return jsonify({
#             'cities': [{
#                 'id': str(city.id), 
#                 'name': city.city_name,
#                 'added_at': city.added_at.isoformat()
#             } for city in cities]
#         })
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
