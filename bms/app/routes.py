from flask import Blueprint, jsonify, request
from app.crud import (
    create_account, get_account, get_account_by_number,
    list_accounts, update_account, delete_account
)
from app.emailer import notify_account_created
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
        
        # Send notification email asynchronously
        notify_account_created(
            account_number=account.number,
            account_name=account.name,
            balance=float(account.balance)
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
@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})