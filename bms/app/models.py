from datetime import datetime
from app.db import db

class Account(db.Model):
    __tablename__ = 'accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(20), unique=True, nullable=False)
    balance = db.Column(db.Numeric(10, 2), default=0.0)
    interest_rate = db.Column(db.Numeric(5, 2), default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Account {self.number}: {self.name}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'number': self.number,
            'balance': float(self.balance),
            'interest_rate': float(self.interest_rate),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }