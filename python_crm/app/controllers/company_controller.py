"""Company controller for handling company-related API endpoints."""

from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models.company import Company

company_bp = Blueprint('company', __name__, url_prefix='/api/company')


@company_bp.route('/', methods=['GET'])
def get_companies():
    """Get all companies for a specific user."""
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
        
        companies = Company.get_all_user_companies(int(user_id))
        return jsonify([company.to_dict() for company in companies])
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@company_bp.route('/', methods=['POST'])
def create_company():
    """Create a new company."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['company_name', 'user_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Parse creation_date if provided
        creation_date = None
        if 'creation_date' in data and data['creation_date']:
            try:
                creation_date = datetime.strptime(data['creation_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        # Create new company
        company = Company(
            company_name=data['company_name'],
            city=data.get('city'),
            sector=data.get('sector'),
            email=data.get('email'),
            creation_date=creation_date,
            user_id=int(data['user_id'])
        )
        
        if company.create_company():
            return jsonify({'message': 'Company created successfully', 'company': company.to_dict()}), 201
        else:
            return jsonify({'error': 'Failed to create company'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@company_bp.route('/<int:company_id>', methods=['PUT'])
def update_company(company_id):
    """Update an existing company."""
    try:
        data = request.get_json()
        
        company = Company.query.get(company_id)
        if not company:
            return jsonify({'error': 'Company not found'}), 404
        
        # Parse creation_date if provided
        if 'creation_date' in data and data['creation_date']:
            try:
                data['creation_date'] = datetime.strptime(data['creation_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        if company.update_company(**data):
            return jsonify({'message': 'Company updated successfully', 'company': company.to_dict()})
        else:
            return jsonify({'error': 'Failed to update company'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@company_bp.route('/<int:company_id>', methods=['DELETE'])
def delete_company(company_id):
    """Delete a company."""
    try:
        if Company.delete_company(company_id):
            return jsonify({'message': 'Company deleted successfully'})
        else:
            return jsonify({'error': 'Company not found or failed to delete'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@company_bp.route('/<int:company_id>', methods=['GET'])
def get_company(company_id):
    """Get a specific company by ID."""
    try:
        company = Company.query.get(company_id)
        if not company:
            return jsonify({'error': 'Company not found'}), 404
        
        return jsonify(company.to_dict())
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500