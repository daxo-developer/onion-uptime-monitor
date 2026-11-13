import aiohttp
from aiohttp_socks import ProxyConnector
import time

async def fetch_onion(url: str, timeout: int = 60) -> dict:
  """
  Fetches a URL via Tor SOCKS5 proxy.
  Returns a dict with status, latency_ms, and error details.
  """
  connector = ProxyConnector.from_url("socks5://127.0.0.1:9050", rdns=True)

  headers = {
       "User-Agent": "OnionUptimeMonitor/0.1 (research; +https://github.com/daxo-developer/onion-uptime-monitor)"
  }

  start_time = time.pref_counter()

  try:
    async with aiohttp.ClientSession(connector=connector) as session:
      async with session.get(url, headers=headers, timeout=timeout) as response:
        latency_ms = (time.perf_counter() - start_time) * 1000
        return {
          "status": response.status,
          "ok": response.status == 200,
          "latency_ms": latency_ms,
          "error_class": None
        }

    except aiohttp.ClientConnectorError:
        return {"status": 0, "ok": False, "latency_ms": 0, "error_class": "connection_refused"}
    except aiohttp.ServerTimeoutError:
        return {"status": 0, "ok": False, "latency_ms": 0, "error_class": "timeout"}
    except Exception as e:
        return {"status": 0, "ok": False, "latency_ms": 0, "error_class": type(e).__name__}
