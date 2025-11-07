import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple
from app.models import Account
from app.config import Config
from app.logger import logger
from flask import current_app

def calculate_batch_total(accounts: List[Account]) -> float:
    """Calculate total balance for a batch of accounts"""
    return sum(float(account.balance) for account in accounts)

def process_batch_threaded(all_accounts: List[Account]) -> List[Tuple[int, float]]:
    """Process accounts in batches using ThreadPoolExecutor"""
    # Allow overriding batch size via Flask app config when available
    try:
        batch_size = int(current_app.config.get('BATCH_SIZE', Config.BATCH_SIZE))
    except RuntimeError:
        batch_size = Config.BATCH_SIZE
    batches = [all_accounts[i:i + batch_size] for i in range(0, len(all_accounts), batch_size)]
    
    results = []
    with ThreadPoolExecutor() as executor:
        batch_futures = []
        for batch_num, batch in enumerate(batches):
            future = executor.submit(calculate_batch_total, batch)
            batch_futures.append((batch_num, future))
        
        for batch_num, future in batch_futures:
            try:
                batch_total = future.result()
                results.append((batch_num, batch_total))
                logger.info("batch_processed", 
                           batch_num=batch_num, 
                           total=batch_total, 
                           processor="threaded")
            except Exception as e:
                logger.error("batch_processing_failed", 
                           batch_num=batch_num, 
                           error=str(e),
                           processor="threaded")
    
    return sorted(results, key=lambda x: x[0])

async def calculate_batch_total_async(batch_num: int, accounts: List[Account]) -> Tuple[int, float]:
    """Calculate total balance for a batch of accounts asynchronously"""
    total = sum(float(account.balance) for account in accounts)
    return batch_num, total

async def process_batch_async(all_accounts: List[Account]) -> List[Tuple[int, float]]:
    """Process accounts in batches using asyncio"""
    try:
        batch_size = int(current_app.config.get('BATCH_SIZE', Config.BATCH_SIZE))
    except RuntimeError:
        batch_size = Config.BATCH_SIZE
    batches = [all_accounts[i:i + batch_size] for i in range(0, len(all_accounts), batch_size)]
    
    tasks = []
    for batch_num, batch in enumerate(batches):
        task = asyncio.create_task(calculate_batch_total_async(batch_num, batch))
        tasks.append(task)
    
    results = []
    for task in asyncio.as_completed(tasks):
        try:
            batch_num, batch_total = await task
            results.append((batch_num, batch_total))
            logger.info("batch_processed", 
                       batch_num=batch_num, 
                       total=batch_total, 
                       processor="async")
        except Exception as e:
            logger.error("batch_processing_failed", 
                       error=str(e),
                       processor="async")
    
    return sorted(results, key=lambda x: x[0])