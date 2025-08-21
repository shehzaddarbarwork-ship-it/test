"""Mail model for the CRM application."""

from datetime import datetime
from config.database import db


class Mail(db.Model):
    """Mail model representing email templates and sent emails."""
    
    __tablename__ = 'mails'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    subject = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    recipient_email = db.Column(db.String(100), nullable=False)
    is_template = db.Column(db.Boolean, default=False)
    is_sent = db.Column(db.Boolean, default=False)
    sent_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, user_id, subject, body, recipient_email, company_id=None, is_template=False):
        """Initialize a new mail."""
        self.user_id = user_id
        self.company_id = company_id
        self.subject = subject
        self.body = body
        self.recipient_email = recipient_email
        self.is_template = is_template
    
    @classmethod
    def get_user_templates(cls, user_id):
        """Get email templates for a specific user."""
        return cls.query.filter_by(user_id=user_id, is_template=True).all()
    
    @classmethod
    def get_sent_emails(cls, user_id):
        """Get sent emails for a specific user."""
        return cls.query.filter_by(user_id=user_id, is_sent=True)\
                       .order_by(cls.sent_at.desc()).all()
    
    def create_mail(self):
        """Create a new mail in the database."""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error creating mail: {e}")
            return False
    
    def mark_as_sent(self):
        """Mark the email as sent."""
        try:
            self.is_sent = True
            self.sent_at = datetime.utcnow()
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error marking mail as sent: {e}")
            return False
    
    @classmethod
    def delete_mail(cls, mail_id):
        """Delete a mail by ID."""
        try:
            mail = cls.query.get(mail_id)
            if mail:
                db.session.delete(mail)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting mail: {e}")
            return False
    
    def to_dict(self):
        """Convert mail to dictionary representation."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'company_id': self.company_id,
            'subject': self.subject,
            'body': self.body,
            'recipient_email': self.recipient_email,
            'is_template': self.is_template,
            'is_sent': self.is_sent,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }