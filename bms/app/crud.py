from sqlalchemy.exc import IntegrityError
from app.db import db
from app.models import Account
from app.exceptions import AccountNotFoundError, DuplicateAccountError, InvalidAccountDataError
from app.logger import logger

def create_account(name: str, number: str, balance: float = 0.0) -> Account:
    """Create a new account"""
    try:
        account = Account(name=name, number=number, balance=balance)
        db.session.add(account)
        db.session.commit()
        logger.info("account_created", account_number=number, name=name)
        return account
    except IntegrityError:
        db.session.rollback()
        logger.error("account_creation_failed", error="duplicate_number", account_number=number)
        raise DuplicateAccountError(f"Account with number {number} already exists")
    except Exception as e:
        db.session.rollback()
        logger.error("account_creation_failed", error=str(e), account_number=number)
        raise InvalidAccountDataError(str(e))

def get_account(account_id: int) -> Account:
    """Get account by ID"""
    account = Account.query.get(account_id)
    if not account:
        logger.error("account_not_found", account_id=account_id)
        raise AccountNotFoundError(f"Account with ID {account_id} not found")
    return account

def get_account_by_number(number: str) -> Account:
    """Get account by account number"""
    account = Account.query.filter_by(number=number).first()
    if not account:
        logger.error("account_not_found", account_number=number)
        raise AccountNotFoundError(f"Account with number {number} not found")
    return account

def list_accounts() -> list[Account]:
    """List all accounts"""
    return Account.query.all()

def update_account(account_id: int, **kwargs) -> Account:
    """Update account details"""
    account = get_account(account_id)
    try:
        for key, value in kwargs.items():
            setattr(account, key, value)
        db.session.commit()
        logger.info("account_updated", account_id=account_id, updates=kwargs)
        return account
    except Exception as e:
        db.session.rollback()
        logger.error("account_update_failed", error=str(e), account_id=account_id)
        raise InvalidAccountDataError(str(e))

def delete_account(account_id: int) -> None:
    """Delete an account"""
    account = get_account(account_id)
    try:
        db.session.delete(account)
        db.session.commit()
        logger.info("account_deleted", account_id=account_id)
    except Exception as e:
        db.session.rollback()
        logger.error("account_deletion_failed", error=str(e), account_id=account_id)
        raise InvalidAccountDataError(str(e))