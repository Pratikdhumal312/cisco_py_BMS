import pytest
from app import create_app
from app.db import db
from app.models import Account
from app.crud import (
    create_account, get_account, get_account_by_number,
    list_accounts, update_account, delete_account
)
from app.exceptions import AccountNotFoundError, DuplicateAccountError

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

def test_create_account(app):
    """Test account creation"""
    with app.app_context():
        account = create_account("Test User", "123456", 1000.0)
        assert account.name == "Test User"
        assert account.number == "123456"
        assert float(account.balance) == 1000.0

def test_duplicate_account(app):
    """Test duplicate account number handling"""
    with app.app_context():
        create_account("Test User 1", "123456", 1000.0)
        with pytest.raises(DuplicateAccountError):
            create_account("Test User 2", "123456", 2000.0)

def test_get_account(app):
    """Test getting account by ID"""
    with app.app_context():
        account = create_account("Test User", "123456", 1000.0)
        retrieved = get_account(account.id)
        assert retrieved.id == account.id
        assert retrieved.name == account.name

def test_get_nonexistent_account(app):
    """Test getting non-existent account"""
    with app.app_context():
        with pytest.raises(AccountNotFoundError):
            get_account(999)

def test_update_account(app):
    """Test updating account details"""
    with app.app_context():
        account = create_account("Test User", "123456", 1000.0)
        updated = update_account(account.id, name="Updated User", balance=2000.0)
        assert updated.name == "Updated User"
        assert float(updated.balance) == 2000.0

def test_delete_account(app):
    """Test account deletion"""
    with app.app_context():
        account = create_account("Test User", "123456", 1000.0)
        delete_account(account.id)
        with pytest.raises(AccountNotFoundError):
            get_account(account.id)

def test_list_accounts(app):
    """Test listing all accounts"""
    with app.app_context():
        create_account("User 1", "111111", 1000.0)
        create_account("User 2", "222222", 2000.0)
        accounts = list_accounts()
        assert len(accounts) == 2