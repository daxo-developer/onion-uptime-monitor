import asyncio
import yaml
import uuid
from tor_monitor.db import init_db, seed_queue, claim_task, complete_task, record_measurement, reschedule_done_tasks
from tor_monitor.fetch import fetch_onion

WORKER_ID = str(uuid.uuid4())[:8]

async def worker_loop(conn, services_map):
    print(f"[{WORKER_ID}] Worker started. Waiting for tasks...")
    
    while True:
        task = claim_task(conn, WORKER_ID)
        
        if task is None:
            reschedule_done_tasks(conn, delay_seconds=300)
            await asyncio.sleep(5)
            continue
            
        service_id, attempts = task
        url = services_map.get(service_id)
        
        if not url:
            print(f"[{WORKER_ID}] Error: No URL found for {service_id}")
            complete_task(conn, service_id, False, attempts + 1)
            continue

        print(f"[{WORKER_ID}] Processing {service_id} (Attempt {attempts + 1})...")
        
        try:
            result = await asyncio.wait_for(fetch_onion(url), timeout=65.0)
        except asyncio.TimeoutError:
            result = {"status": 0, "ok": False, "latency_ms": 0, "error_class": "asyncio_timeout"}
            
        record_measurement(conn, service_id, result)
        
        if result["ok"]:
            print(f"[{WORKER_ID}] Success: {service_id} - {result['latency_ms']:.2f} ms")
            complete_task(conn, service_id, True, attempts)
        else:
            print(f"[{WORKER_ID}] Failed: {service_id} - {result['error_class']}")
            complete_task(conn, service_id, False, attempts + 1)
            
        await asyncio.sleep(2)

async def main():
    with open("services.yaml", "r") as f:
        config = yaml.safe_load(f)
        services = config["services"]
        
    services_map = {s["id"]: s["url"] for s in services}
    
    conn = init_db()
    seed_queue(conn, services)
    
    print(f"Loaded {len(services)} services. Starting monitor...")
    await worker_loop(conn, services_map)

if __name__ == "__main__":
    asyncio.run(main())
