"""Mail controller for handling email-related API endpoints."""

from flask import Blueprint, request, jsonify
from app.models.mail import Mail

mail_bp = Blueprint('mail', __name__, url_prefix='/api/mail')


@mail_bp.route('/templates/<int:user_id>', methods=['GET'])
def get_user_templates(user_id):
    """Get email templates for a specific user."""
    try:
        templates = Mail.get_user_templates(user_id)
        return jsonify([template.to_dict() for template in templates])
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@mail_bp.route('/sent/<int:user_id>', methods=['GET'])
def get_sent_emails(user_id):
    """Get sent emails for a specific user."""
    try:
        sent_emails = Mail.get_sent_emails(user_id)
        return jsonify([email.to_dict() for email in sent_emails])
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@mail_bp.route('/', methods=['POST'])
def create_mail():
    """Create a new email or template."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['user_id', 'subject', 'body', 'recipient_email']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create new mail
        mail = Mail(
            user_id=int(data['user_id']),
            subject=data['subject'],
            body=data['body'],
            recipient_email=data['recipient_email'],
            company_id=data.get('company_id'),
            is_template=data.get('is_template', False)
        )
        
        if mail.create_mail():
            return jsonify({
                'message': 'Email created successfully',
                'mail': mail.to_dict()
            }), 201
        else:
            return jsonify({'error': 'Failed to create email'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@mail_bp.route('/<int:mail_id>/send', methods=['POST'])
def send_mail(mail_id):
    """Mark an email as sent (simulated sending)."""
    try:
        mail = Mail.query.get(mail_id)
        if not mail:
            return jsonify({'error': 'Email not found'}), 404
        
        if mail.mark_as_sent():
            return jsonify({
                'message': 'Email sent successfully',
                'mail': mail.to_dict()
            })
        else:
            return jsonify({'error': 'Failed to send email'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@mail_bp.route('/<int:mail_id>', methods=['DELETE'])
def delete_mail(mail_id):
    """Delete an email."""
    try:
        if Mail.delete_mail(mail_id):
            return jsonify({'message': 'Email deleted successfully'})
        else:
            return jsonify({'error': 'Email not found or failed to delete'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@mail_bp.route('/<int:mail_id>', methods=['GET'])
def get_mail(mail_id):
    """Get a specific email by ID."""
    try:
        mail = Mail.query.get(mail_id)
        if not mail:
            return jsonify({'error': 'Email not found'}), 404
        
        return jsonify(mail.to_dict())
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@mail_bp.route('/<int:mail_id>', methods=['PUT'])
def update_mail(mail_id):
    """Update an existing email."""
    try:
        data = request.get_json()
        
        mail = Mail.query.get(mail_id)
        if not mail:
            return jsonify({'error': 'Email not found'}), 404
        
        # Update fields if provided
        if 'subject' in data:
            mail.subject = data['subject']
        if 'body' in data:
            mail.body = data['body']
        if 'recipient_email' in data:
            mail.recipient_email = data['recipient_email']
        if 'is_template' in data:
            mail.is_template = data['is_template']
        
        try:
            from config.database import db
            db.session.commit()
            return jsonify({
                'message': 'Email updated successfully',
                'mail': mail.to_dict()
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to update email'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500