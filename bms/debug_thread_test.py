from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace
from app.batch_calc import process_batch_threaded

sample_accounts = [SimpleNamespace(id=i+1,name=f"User {i}",number=f"ACC{i}",balance=1000.0*(i+1)) for i in range(5)]

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(process_batch_threaded, sample_accounts) for _ in range(10)]
    results = [f.result() for f in futures]

for i, r in enumerate(results):
    print(i, len(r), r)
