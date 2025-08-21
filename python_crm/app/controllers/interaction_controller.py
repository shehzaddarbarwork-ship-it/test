"""Interaction controller for handling interaction-related API endpoints."""

from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models.interaction import Interaction

interaction_bp = Blueprint('interaction', __name__, url_prefix='/api/interaction')


@interaction_bp.route('/company/<int:company_id>', methods=['GET'])
def get_company_interactions(company_id):
    """Get interactions for a specific company."""
    try:
        limit = request.args.get('limit', 10, type=int)
        interactions = Interaction.get_company_interactions(company_id, limit)
        return jsonify([interaction.to_dict() for interaction in interactions])
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@interaction_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_interactions(user_id):
    """Get interactions for a specific user."""
    try:
        limit = request.args.get('limit', 10, type=int)
        interactions = Interaction.get_user_interactions(user_id, limit)
        return jsonify([interaction.to_dict() for interaction in interactions])
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@interaction_bp.route('/', methods=['POST'])
def create_interaction():
    """Create a new interaction."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['company_id', 'user_id', 'interaction_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Parse interaction_date if provided
        interaction_date = None
        if 'interaction_date' in data and data['interaction_date']:
            try:
                interaction_date = datetime.fromisoformat(data['interaction_date'])
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use ISO format'}), 400
        
        # Create new interaction
        interaction = Interaction(
            company_id=int(data['company_id']),
            user_id=int(data['user_id']),
            interaction_type=data['interaction_type'],
            description=data.get('description', ''),
            interaction_date=interaction_date
        )
        
        if interaction.create_interaction():
            return jsonify({
                'message': 'Interaction created successfully',
                'interaction': interaction.to_dict()
            }), 201
        else:
            return jsonify({'error': 'Failed to create interaction'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@interaction_bp.route('/<int:interaction_id>', methods=['DELETE'])
def delete_interaction(interaction_id):
    """Delete an interaction."""
    try:
        if Interaction.delete_interaction(interaction_id):
            return jsonify({'message': 'Interaction deleted successfully'})
        else:
            return jsonify({'error': 'Interaction not found or failed to delete'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@interaction_bp.route('/<int:interaction_id>', methods=['GET'])
def get_interaction(interaction_id):
    """Get a specific interaction by ID."""
    try:
        interaction = Interaction.query.get(interaction_id)
        if not interaction:
            return jsonify({'error': 'Interaction not found'}), 404
        
        return jsonify(interaction.to_dict())
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@interaction_bp.route('/<int:interaction_id>', methods=['PUT'])
def update_interaction(interaction_id):
    """Update an existing interaction."""
    try:
        data = request.get_json()
        
        interaction = Interaction.query.get(interaction_id)
        if not interaction:
            return jsonify({'error': 'Interaction not found'}), 404
        
        # Update fields if provided
        if 'interaction_type' in data:
            interaction.interaction_type = data['interaction_type']
        if 'description' in data:
            interaction.description = data['description']
        if 'interaction_date' in data and data['interaction_date']:
            try:
                interaction.interaction_date = datetime.fromisoformat(data['interaction_date'])
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use ISO format'}), 400
        
        try:
            from config.database import db
            db.session.commit()
            return jsonify({
                'message': 'Interaction updated successfully',
                'interaction': interaction.to_dict()
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to update interaction'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500