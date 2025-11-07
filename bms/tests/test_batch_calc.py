import pytest
from concurrent.futures import ThreadPoolExecutor
import asyncio
from app import create_app
from app.db import db
from app.models import Account
from app.batch_calc import (
    calculate_batch_total,
    process_batch_threaded,
    process_batch_async
)

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['BATCH_SIZE'] = 2
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def sample_accounts(app):
    """Create sample accounts for testing"""
    with app.app_context():
        accounts = []
        for i in range(5):
            account = Account(
                name=f"User {i}",
                number=f"ACC{i}",
                balance=1000.0 * (i + 1)
            )
            db.session.add(account)
            accounts.append(account)
        db.session.commit()

        # Ensure module-level Config respects the test's batch size
        from app.config import Config as AppConfig
        AppConfig.BATCH_SIZE = app.config.get('BATCH_SIZE', AppConfig.BATCH_SIZE)

        # Return lightweight snapshots (detached objects may be expired)
        from types import SimpleNamespace
        snapshots = []
        for acc in accounts:
            snapshots.append(SimpleNamespace(
                id=acc.id,
                name=acc.name,
                number=acc.number,
                balance=float(acc.balance)
            ))
        return snapshots

def test_calculate_batch_total(sample_accounts):
    """Test calculating total for a batch of accounts"""
    batch = sample_accounts[:2]  # First two accounts
    total = calculate_batch_total(batch)
    assert total == 3000.0  # 1000 + 2000

def test_process_batch_threaded(sample_accounts):
    """Test processing accounts in batches using threads"""
    results = process_batch_threaded(sample_accounts)
    
    assert len(results) == 3  # 5 accounts with batch size 2 = 3 batches
    
    # Verify batch totals
    assert results[0][1] == 3000.0  # Batch 0: 1000 + 2000
    assert results[1][1] == 7000.0  # Batch 1: 3000 + 4000
    assert results[2][1] == 5000.0  # Batch 2: 5000

@pytest.mark.asyncio
async def test_process_batch_async(sample_accounts):
    """Test processing accounts in batches using asyncio"""
    results = await process_batch_async(sample_accounts)
    
    assert len(results) == 3  # 5 accounts with batch size 2 = 3 batches
    
    # Verify batch totals
    assert results[0][1] == 3000.0  # Batch 0: 1000 + 2000
    assert results[1][1] == 7000.0  # Batch 1: 3000 + 4000
    assert results[2][1] == 5000.0  # Batch 2: 5000

def test_thread_pool_stress(sample_accounts):
    """Stress test the thread pool implementation"""
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for _ in range(10):  # Run multiple batch processes concurrently
            future = executor.submit(process_batch_threaded, sample_accounts)
            futures.append(future)
        
        # Verify all processes complete successfully
        results = [future.result() for future in futures]
        assert all(len(r) == 3 for r in results)  # Each should have 3 batches

@pytest.mark.asyncio
async def test_async_stress():
    """Stress test the async implementation"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['BATCH_SIZE'] = 2
    
    with app.app_context():
        # Create test accounts
        accounts = []
        for i in range(5):
            account = Account(
                name=f"User {i}",
                number=f"ACC{i}",
                balance=1000.0 * (i + 1)
            )
            db.session.add(account)
            accounts.append(account)
        db.session.commit()
        
        # Run multiple async batch processes concurrently
        tasks = [process_batch_async(accounts) for _ in range(10)]
        results = await asyncio.gather(*tasks)
        
        assert all(len(r) == 3 for r in results)  # Each should have 3 batches