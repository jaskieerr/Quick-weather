from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required, current_user
from models import User, SavedCity, db
from sqlalchemy.exc import IntegrityError

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    """Render main page"""
    return render_template('main.html')

@views_bp.route('/homepage')
@login_required
def homepage():
    """Render homepage for logged-in users"""
    return render_template('homepage.html')

@views_bp.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    """Update user profile information"""
    try:
        data = request.json
        
        # Check if email is being changed and if it's already taken
        if 'email' in data and data['email'] != current_user.email:
            if User.query.filter_by(email=data['email']).first():
                return jsonify({'error': 'Email already in use'}), 400
        
        current_user.full_name = data.get('username', current_user.full_name)
        current_user.email = data.get('email', current_user.email)
        
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@views_bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    """Change user password"""
    try:
        data = request.json
        
        if not bcrypt.check_password_hash(current_user.password_hash, data['current_password']):
            return jsonify({'error': 'Current password is incorrect'}), 400
        
        new_password_hash = bcrypt.generate_password_hash(data['new_password']).decode('utf-8')
        current_user.password_hash = new_password_hash
        db.session.commit()
        
        return jsonify({'message': 'Password updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@views_bp.route('/save_city', methods=['POST'])
@login_required
def save_city():
    """Save a city to user's favorites"""
    try:
        data = request.json
        
        # Check if city is already saved
        existing_city = SavedCity.query.filter_by(
            user_id=current_user.id,
            city_name=data['city_name']
        ).first()
        
        if existing_city:
            return jsonify({'error': 'City already saved'}), 400
        
        new_city = SavedCity(
            city_name=data['city_name'],
            user_id=current_user.id
        )
        
        db.session.add(new_city)
        db.session.commit()
        
        return jsonify({'message': 'City saved successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@views_bp.route('/get_saved_cities')
@login_required
def get_saved_cities():
    """Get user's saved cities"""
    try:
        cities = SavedCity.query.filter_by(user_id=current_user.id).order_by(SavedCity.added_at.desc()).all()
        return jsonify({
            'cities': [{
                'id': str(city.id), 
                'name': city.city_name,
                'added_at': city.added_at.isoformat()
            } for city in cities]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500