"""Interaction model for the CRM application."""

from datetime import datetime
from config.database import db


class Interaction(db.Model):
    """Interaction model representing interactions with companies."""
    
    __tablename__ = 'interactions'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    interaction_type = db.Column(db.String(50), nullable=False)  # call, email, meeting, etc.
    description = db.Column(db.Text)
    interaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, company_id, user_id, interaction_type, description, interaction_date=None):
        """Initialize a new interaction."""
        self.company_id = company_id
        self.user_id = user_id
        self.interaction_type = interaction_type
        self.description = description
        if interaction_date:
            self.interaction_date = interaction_date
    
    @classmethod
    def get_company_interactions(cls, company_id, limit=10):
        """Get interactions for a specific company."""
        return cls.query.filter_by(company_id=company_id)\
                       .order_by(cls.interaction_date.desc())\
                       .limit(limit).all()
    
    @classmethod
    def get_user_interactions(cls, user_id, limit=10):
        """Get interactions for a specific user."""
        return cls.query.filter_by(user_id=user_id)\
                       .order_by(cls.interaction_date.desc())\
                       .limit(limit).all()
    
    def create_interaction(self):
        """Create a new interaction in the database."""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error creating interaction: {e}")
            return False
    
    @classmethod
    def delete_interaction(cls, interaction_id):
        """Delete an interaction by ID."""
        try:
            interaction = cls.query.get(interaction_id)
            if interaction:
                db.session.delete(interaction)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting interaction: {e}")
            return False
    
    def to_dict(self):
        """Convert interaction to dictionary representation."""
        return {
            'id': self.id,
            'company_id': self.company_id,
            'user_id': self.user_id,
            'interaction_type': self.interaction_type,
            'description': self.description,
            'interaction_date': self.interaction_date.isoformat() if self.interaction_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }