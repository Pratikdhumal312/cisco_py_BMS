class BMSError(Exception):
    """Base exception for BMS application"""
    pass

class AccountNotFoundError(BMSError):
    """Raised when an account is not found"""
    pass

class DuplicateAccountError(BMSError):
    """Raised when trying to create an account with existing number"""
    pass

class InsufficientFundsError(BMSError):
    """Raised when account has insufficient funds for operation"""
    pass

class InvalidAccountDataError(BMSError):
    """Raised when account data is invalid"""
    pass

class EmailError(BMSError):
    """Raised when there is an error sending email"""
    pass

class ScrapingError(BMSError):
    """Raised when there is an error during web scraping"""
    pass