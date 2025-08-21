"""Company model for the CRM application."""

from datetime import datetime
from config.database import db


class Company(db.Model):
    """Company model representing companies in the CRM system."""
    
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50))
    sector = db.Column(db.String(50))
    email = db.Column(db.String(100))
    creation_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    interactions = db.relationship('Interaction', backref='company', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, company_name, city, sector, email, creation_date, user_id):
        """Initialize a new company."""
        self.company_name = company_name
        self.city = city
        self.sector = sector
        self.email = email
        self.creation_date = creation_date
        self.user_id = user_id
    
    @classmethod
    def get_all_user_companies(cls, user_id):
        """Get all companies for a specific user."""
        return cls.query.filter_by(user_id=user_id).all()
    
    def create_company(self):
        """Create a new company in the database."""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error creating company: {e}")
            return False
    
    @classmethod
    def delete_company(cls, company_id):
        """Delete a company by ID."""
        try:
            company = cls.query.get(company_id)
            if company:
                db.session.delete(company)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting company: {e}")
            return False
    
    def update_company(self, **kwargs):
        """Update company information."""
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error updating company: {e}")
            return False
    
    def to_dict(self):
        """Convert company to dictionary representation."""
        return {
            'id': self.id,
            'company_name': self.company_name,
            'city': self.city,
            'sector': self.sector,
            'email': self.email,
            'creation_date': self.creation_date.isoformat() if self.creation_date else None,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }