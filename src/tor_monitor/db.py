import sqlite3
import time

def init_db(db_path: str = "monitor.db"):
    """Initializes the SQLite database with WAL mode."""
    conn = sqlite3.connect(db_path)
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
    conn.commit()
    return conn

def record_measurement(conn: sqlite3.Connection, service_id: str, result: dict):
    """Inserts a measurement result into the database."""
    conn.execute(
        "INSERT INTO measurements (service_id, ts, ok, status, latency_ms, error_class) VALUES (?, ?, ?, ?, ?, ?)",
        (service_id, int(time.time()), int(result["ok"]), result["status"], result["latency_ms"], result["error_class"])
    )
    conn.commit()
