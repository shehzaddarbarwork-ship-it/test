"""User controller for handling user authentication and management."""

from flask import Blueprint, request, jsonify, session
from app.models.user import User

user_bp = Blueprint('user', __name__, url_prefix='/api/user')


@user_bp.route('/signup', methods=['POST'])
def signup():
    """Register a new user."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'password', 'email']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if user already exists
        existing_user = User.check_already_exist(data['username'], data['email'])
        if existing_user:
            return jsonify({'error': 'User with this username or email already exists'}), 409
        
        # Create new user
        user = User(
            username=data['username'],
            password=data['password'],
            email=data['email']
        )
        
        if user.create_user():
            return jsonify({
                'message': 'User created successfully',
                'user': user.to_dict()
            }), 201
        else:
            return jsonify({'error': 'Failed to create user'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/login', methods=['POST'])
def login():
    """Authenticate a user."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password are required'}), 400
        
        # Find user by username
        user = User.get_user_by_username(data['username'])
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # Store user session
        session['user_id'] = user.id
        session['username'] = user.username
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/logout', methods=['POST'])
def logout():
    """Log out the current user."""
    try:
        session.clear()
        return jsonify({'message': 'Logout successful'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/profile', methods=['GET'])
def get_profile():
    """Get the current user's profile."""
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not authenticated'}), 401
        
        user = User.get_user(session['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict())
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID."""
    try:
        user = User.get_user(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict())
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/check-auth', methods=['GET'])
def check_auth():
    """Check if user is authenticated."""
    try:
        if 'user_id' in session:
            return jsonify({
                'authenticated': True,
                'user_id': session['user_id'],
                'username': session['username']
            })
        else:
            return jsonify({'authenticated': False})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500