# Onion Uptime Monitor

**Mission:** A research tool to measure the avaliability and latency of public, legal Tor onion services (Tor project, DuckDuckGo, Debian, SecureDrop instances) and compare them against their clearnet mirrors.

**Core Question:** How stable are onion services over time compared to the clearnet, and how does their avaliability fluctuate by time of day?

## Tech Stack
* **Async Core:** asyncio, aiohttp, aiohttp-socks (SOCKS5 via Tor, rdns=True).
* **Storage:** SQLite (WAL mode) with an atomic task queue.
* **Analytics:** Python (percentiles, correlation, uptime aggregation).
* **Dashboard:** Vanilla JS / d3.js / Chart.js

## Ethical Guidelines
* Strict compliance with the Tor Research Safety Board guidelines.
* **Metadata only.** No content scraping.
* **Public and legal services only** (officially published mirrors).
* Honest User-Agent and rate limiting per host.

## Setup (WIP)
`pip install -e ".[dev]"`
