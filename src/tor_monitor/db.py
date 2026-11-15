import sqlite3
import time
import random

def init_db(db_path: str = "monitor.db"):
    """Initializes SQLite with WAL mode and queue tables."""
    conn = sqlite3.connect(db_path, isolation_level=None)
    conn.execute("PRAGMA journal_mode=WAL;")
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_id TEXT NOT NULL,
            ts INTEGER NOT NULL,
            ok INTEGER NOT NULL,
            status INTEGER,
            latency_ms REAL,
            error_class TEXT
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_id TEXT NOT NULL UNIQUE,
            state TEXT CHECK(state IN ('pending', 'in_progress', 'done', 'failed')) DEFAULT 'pending',
            attempts INTEGER DEFAULT 0,
            next_attempt_at INTEGER,
            worker_id TEXT
        )
    """)
    return conn

def seed_queue(conn: sqlite3.Connection, services: list):
    for svc in services:
        conn.execute(
            "INSERT OR IGNORE INTO queue (service_id, state, next_attempt_at) VALUES (?, 'pending', ?)",
            (svc['id'], int(time.time()))
        )

def claim_task(conn: sqlite3.Connection, worker_id: str):
    conn.execute("BEGIN IMMEDIATE;")
    cursor = conn.execute("""
        UPDATE queue 
        SET state = 'in_progress', worker_id = ?
        WHERE service_id = (
            SELECT service_id FROM queue 
            WHERE state = 'pending' AND next_attempt_at <= ? 
            ORDER BY next_attempt_at LIMIT 1
        )
        RETURNING service_id, attempts
    """, (worker_id, int(time.time())))
    row = cursor.fetchone()
    conn.execute("COMMIT;")
    return row

def complete_task(conn: sqlite3.Connection, service_id: str, success: bool, attempts: int):
    if success:
        conn.execute("UPDATE queue SET state = 'done', worker_id = NULL WHERE service_id = ?", (service_id,))
    else:
        delay = (2 ** attempts) * 10 + random.randint(1, 5)
        next_time = int(time.time()) + delay
        conn.execute(
            "UPDATE queue SET state = 'pending', worker_id = NULL, attempts = ?, next_attempt_at = ? WHERE service_id = ?",
            (attempts, next_time, service_id)
        )

def reschedule_done_tasks(conn: sqlite3.Connection, delay_seconds: int = 300):
    """ВАЖНО: Возвращает выполненные задачи обратно в очередь с задержкой."""
    next_time = int(time.time()) + delay_seconds
    conn.execute("""
        UPDATE queue 
        SET state = 'pending', attempts = 0, next_attempt_at = ? 
        WHERE state = 'done'
    """, (next_time,))

def record_measurement(conn: sqlite3.Connection, service_id: str, result: dict):
    conn.execute(
        "INSERT INTO measurements (service_id, ts, ok, status, latency_ms, error_class) VALUES (?, ?, ?, ?, ?, ?)",
        (service_id, int(time.time()), int(result["ok"]), result["status"], result["latency_ms"], result["error_class"])
    )
