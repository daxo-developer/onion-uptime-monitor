# Onion Uptime Monitor

[![Tests](https://github.com/daxo-developer/onion-uptime-monitor/actions/workflows/test.yml/badge.svg)](https://github.com/daxo-developer/onion-uptime-monitor/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Live Dashboard:** [https://daxo-developer.github.io/onion-uptime-monitor/](https://daxo-developer.github.io/onion-uptime-monitor/)

## Architecture

```
graph LR
    W[Monitor Worker] -->|SOCKS5| T[Tor Proxy]
    T -->|Onion| O[.onion Services]
    T -->|Clearnet| C[Clearnet Mirrors]
    W -->|Write| DB[(SQLite WAL)]
    DB -->|Aggregate| J[analytics.json]
    J -->|Deploy| GH[GitHub Pages Dashboard]
```

## Mission

A research tool to measure the availability, latency (TTFB vs Total), and clearnet parity of public Tor onion services.

## Core Question

How stable are onion services over time compared to the clearnet, and how does their availability fluctuate by time of day?

# Tech Stack

· Async Core: asyncio, aiohttp, aiohttp-socks (SOCKS5 via Tor, rdns=True).
· Storage: SQLite (WAL mode) with an atomic task queue.
· Analytics: Python (percentiles, correlation, uptime aggregation).
· Dashboard: Vanilla JS / Chart.js.
· Deployment: Docker & GitHub Actions.

## Ethical Guidelines

· Strict compliance with the Tor Research Safety Board guidelines.
· Metadata only. No content scraping.
· Public and legal services only (officially published mirrors).
· Honest User-Agent and rate limiting per host.

# Setup (Local)

```
pip install -e ".[dev]"
python -m tor_monitor.monitor
```

# Setup (Docker)

```
docker-compose up -d
```

Troubleshooting: Bypassing Censorship with Bridges

If your ISP blocks direct connections to the Tor network, you can configure obfs4 bridges to mask your traffic.

1. Install lyrebird (successor of obfs4proxy in Termux):

```
pkg install obfs4proxy -y
```

2. Configure Tor to use bridges by appending to your torrc:

```
UseBridges 1
ClientTransportPlugin obfs4 exec /data/data/com.termux/files/usr/bin/lyrebird
Bridge obfs4 <YOUR_BRIDGE_IP:PORT> <FINGERPRINT> cert=<CERT> iat-mode=1
```
(Note: Real bridge addresses are intentionally omitted from this public repository for operational security. Publicly exposing active bridges allows censors to block them. Request private bridges at bridges.torproject.org).

3. Restart Tor and verify connection.

## Proof of Work

First successful real-world measurement (via obfs4 bridge):

```
Result: {'status': 200, 'ok': True, 'ttfb_ms': 2150.4, 'latency_ms': 4301.8, 'error_class': None}
```
