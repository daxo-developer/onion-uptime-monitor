import sqlite3
import statistics
import json

def analyze_uptime(db_path: str = "monitor.db") -> dict:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT service_id FROM measurements")
    services = [row[0] for row in cursor.fetchall()]

    results = {}
    for svc in services:
        cursor.execute("SELECT ok, ttfb_ms, latency_ms, error_class FROM measurements WHERE service_id = ?", (svc,))
        rows = cursor.fetchall()
        
        if not rows: continue

        total = len(rows)
        successful = sum(1 for r in rows if r[0] == 1)
        uptime_pct = (successful / total) * 100

        latencies = [r[2] for r in rows if r[0] == 1 and r[2] is not None]
        ttfbs = [r[1] for r in rows if r[0] == 1 and r[1] is not None]
        
        if latencies:
            latencies.sort()
            p50_lat = statistics.median(latencies)
            p95_lat = latencies[min(int(len(latencies) * 0.95), len(latencies) - 1)]
        else: p50_lat, p95_lat = 0, 0

        if ttfbs:
            ttfbs.sort()
            p50_ttfb = statistics.median(ttfbs)
        else: p50_ttfb = 0

        errors = {}
        for r in rows:
            if r[0] == 0 and r[3]:
                errors[r[3]] = errors.get(r[3], 0) + 1

        results[svc] = {
            "total_checks": total,
            "uptime_pct": round(uptime_pct, 2),
            "ttfb_p50_ms": round(p50_ttfb, 2),
            "latency_p50_ms": round(p50_lat, 2),
            "latency_p95_ms": round(p95_lat, 2),
            "errors": errors
        }

    conn.close()
    return results

if __name__ == "__main__":
    stats = analyze_uptime()
    print(json.dumps(stats, indent=4))
    with open("analytics.json", "w") as f:
        json.dump(stats, f, indent=4)
    print("\n[INFO] Analytics saved to analytics.json")
