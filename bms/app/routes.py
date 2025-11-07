from flask import Blueprint, jsonify, request
from app.crud import (
    create_account, get_account, get_account_by_number,
    list_accounts, update_account, delete_account
)
# notifications are handled by CRUD layer (app.crud) to keep behavior consistent
from app.exceptions import (
    BMSError, AccountNotFoundError, DuplicateAccountError,
    InvalidAccountDataError
)
from app.logger import logger

bp = Blueprint('api', __name__)

@bp.errorhandler(BMSError)
def handle_bms_error(error):
    """Handle custom BMS exceptions"""
    return jsonify({'error': str(error)}), 400

@bp.route('/accounts', methods=['POST'])
def create_new_account():
    """Create a new account"""
    data = request.get_json()
    
    try:
        account = create_account(
            name=data['name'],
            number=data['number'],
            balance=float(data.get('balance', 0.0))
        )
        
        return jsonify(account.to_dict()), 201
    
    except (KeyError, ValueError) as e:
        return jsonify({'error': f'Invalid input: {str(e)}'}), 400
    except DuplicateAccountError as e:
        return jsonify({'error': str(e)}), 409

@bp.route('/accounts/<int:account_id>', methods=['GET'])
def get_account_by_id(account_id):
    """Get account by ID"""
    try:
        account = get_account(account_id)
        return jsonify(account.to_dict())
    except AccountNotFoundError as e:
        return jsonify({'error': str(e)}), 404

@bp.route('/accounts/number/<string:account_number>', methods=['GET'])
def find_account_by_number(account_number):
    """Get account by account number"""
    try:
        account = get_account_by_number(account_number)
        return jsonify(account.to_dict())
    except AccountNotFoundError as e:
        return jsonify({'error': str(e)}), 404

@bp.route('/accounts', methods=['GET'])
def get_all_accounts():
    """List all accounts"""
    accounts = list_accounts()
    return jsonify([account.to_dict() for account in accounts])

@bp.route('/accounts/<int:account_id>', methods=['PUT'])
def update_account_details(account_id):
    """Update account details"""
    data = request.get_json()
    
    try:
        # Filter out None values and convert balance to float if present
        updates = {k: float(v) if k == 'balance' else v 
                  for k, v in data.items() 
                  if v is not None}
        
        account = update_account(account_id, **updates)
        return jsonify(account.to_dict())
    
    except (ValueError, InvalidAccountDataError) as e:
        return jsonify({'error': str(e)}), 400
    except AccountNotFoundError as e:
        return jsonify({'error': str(e)}), 404

@bp.route('/accounts/<int:account_id>', methods=['DELETE'])
def remove_account(account_id):
    """Delete an account"""
    try:
        delete_account(account_id)
        return '', 204
    except AccountNotFoundError as e:
        return jsonify({'error': str(e)}), 404

# Health check endpoint
@bp.route('/accounts/batch', methods=['POST'])
def create_multiple_accounts():
    """Create multiple accounts in one request"""
    data = request.get_json()
    if not isinstance(data, list):
        return jsonify({'error': 'Request body must be an array of accounts'}), 400
    
    results = []
    errors = []
    
    for idx, account_data in enumerate(data):
        try:
            account = create_account(
                name=account_data['name'],
                number=account_data['number'],
                balance=float(account_data.get('balance', 0.0))
            )
            
            results.append(account.to_dict())
        except (KeyError, ValueError, DuplicateAccountError) as e:
            errors.append({
                'index': idx,
                'data': account_data,
                'error': str(e)
            })
    
    response = {
        'success': results,
        'errors': errors
    }
    
    # Return 201 if at least one account was created, 400 if all failed
    status_code = 201 if results else 400
    return jsonify(response), status_code

@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})