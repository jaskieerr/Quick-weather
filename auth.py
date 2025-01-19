from flask import Blueprint, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from models import User, db
from app import bcrypt
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """Handle user registration"""
    try:
        data = request.form
        
        # Check if user already exists
        if User.query.filter_by(email=data['signup_email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create new user
        hashed_password = bcrypt.generate_password_hash(data['signup_passwd']).decode('utf-8')
        new_user = User(
            email=data['signup_email'],
            password_hash=hashed_password,
            full_name=data['full_name']
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return jsonify({'message': 'Registration successful'}), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Handle user login"""
    try:
        data = request.form
        user = User.query.filter_by(email=data['login_email']).first()
        
        if user and bcrypt.check_password_hash(user.password_hash, data['login_passwd']):
            login_user(user)
            return jsonify({'message': 'Login successful'}), 200
        
        return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout')
@login_required
def logout():
    """Handle user logout"""
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/delete_account', methods=['DELETE'])
@login_required
def delete_account():
    """Handle account deletion"""
    try:
        user = current_user
        db.session.delete(user)
        db.session.commit()
        logout_user()
        return jsonify({'message': 'Account deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500