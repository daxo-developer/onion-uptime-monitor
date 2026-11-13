# Onion Uptime Monitor

## Mission

A research tool to measure the availability and latency of public, legal Tor onion services (Tor Project, DuckDuckGo, Debian, SecureDrop instances) and compare them against their clearnet mirrors.

## Core Question

How stable are onion services over time compared to the clearnet, and how does their availability fluctuate by time of day?

## Tech Stack

* **Async Core:** asyncio, aiohttp, aiohttp-socks (SOCKS5 via Tor, rdns=True).
* **Storage:** SQLite (WAL mode) with an atomic task queue.
* **Analytics:** Python (percentiles, correlation, uptime aggregation).
* **Dashboard:** Vanilla JS / d3.js / Chart.js.

## Ethical Guidelines

* Strict compliance with the Tor Research Safety Board guidelines.
* Metadata only. No content scraping.
* Public and legal services only (officially published mirrors).
* Honest User-Agent and rate limiting per host.

## Setup (WIP)

```
pip install -e ".[dev]"
```

## Troubleshooting: Bypassing Censorship with Bridges

If your ISP blocks direct connections to the Tor network, you can configure `obfs4` bridges to mask your traffic. *(Note: Bridges are ephemeral and may expire; always request fresh ones from bridges.torproject.org if these fail).*

1. Install `lyrebird` (successor of obfs4proxy in Termux):
   ```
   pkg install obfs4proxy -y
   ```

2. Configure Tor to use bridges by appending to your torrc:
   ```
   UseBridges 1
   ClientTransportPlugin obfs4 exec /data/data/com.termux/files/usr/bin/lyrebird
   Bridge obfs4 185.177.207.199:12199 CE9FB471CD33ADFD45D1851E3FB3B6E8B8C8F0CD cert=b0194UWG2T7IX0Y6hBUbxA30LjyxFixxZuZv/C2vtvzSC9tarpB0OO+JIuTRbhzGqXfHbg iat-mode=1
   ```

3. Restart Tor and verify connection.

## Proof of Work

First successful real-world measurement (via obfs4 bridge):
```
Result: {'status': 200, 'ok': True, 'latency_ms': 4301.832497934811, 'error_class': None}
```
