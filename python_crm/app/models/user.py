"""User model for the CRM application."""

from datetime import datetime
from config.database import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """User model representing users in the CRM system."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(50), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    companies = db.relationship('Company', backref='user', lazy=True)
    
    def __init__(self, username, password, email):
        """Initialize a new user."""
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email
    
    def check_password(self, password):
        """Check if provided password matches the user's password."""
        return check_password_hash(self.password, password)
    
    @classmethod
    def check_already_exist(cls, username, email):
        """Check if a user with the given username or email already exists."""
        return cls.query.filter(
            (cls.username == username) | (cls.email == email)
        ).first()
    
    @classmethod
    def get_user(cls, user_id):
        """Get a user by ID."""
        return cls.query.get(user_id)
    
    @classmethod
    def get_user_by_username(cls, username):
        """Get a user by username."""
        return cls.query.filter_by(username=username).first()
    
    def create_user(self):
        """Create a new user in the database."""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error creating user: {e}")
            return False
    
    def to_dict(self):
        """Convert user to dictionary representation."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }