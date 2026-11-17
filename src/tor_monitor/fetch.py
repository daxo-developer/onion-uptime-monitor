import aiohttp
from aiohttp_socks import ProxyConnector
import time
import os

async def fetch_onion(url: str, timeout: int = 60) -> dict:
    proxy_url = os.getenv("TOR_PROXY", "socks5://127.0.0.1:9050")
    connector = ProxyConnector.from_url(proxy_url, rdns=True)
    
    headers = {
        "User-Agent": "OnionUptimeMonitor/0.2 (research; +https://github.com/daxo-developer/onion-uptime-monitor)"
    }
    
    start_time = time.perf_counter()
    
    try:
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url, headers=headers, timeout=timeout) as response:
                ttfb = (time.perf_counter() - start_time) * 1000
                await response.read()
                total_time = (time.perf_counter() - start_time) * 1000
                
                return {
                    "status": response.status,
                    "ok": response.status == 200,
                    "ttfb_ms": ttfb,
                    "latency_ms": total_time,
                    "error_class": None
                }
    except Exception as e:
        return {"status": 0, "ok": False, "ttfb_ms": 0, "latency_ms": 0, "error_class": type(e).__name__}
