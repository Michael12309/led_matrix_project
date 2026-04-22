import requests
import time

LATITUDE = 42.8864
LONGITUDE = -78.8784

UV_URL = (
    f"https://api.open-meteo.com/v1/forecast"
    f"?latitude={LATITUDE}&longitude={LONGITUDE}"
    f"&current=uv_index&timezone=auto&forecast_days=1"
)

_cached_uv = 0
_last_fetch = 0
CACHE_SECONDS = 600

def get_uv_index():
    global _cached_uv, _last_fetch
    now = time.time()
    if now - _last_fetch < CACHE_SECONDS:
        return _cached_uv
    try:
        resp = requests.get(UV_URL, timeout=5)
        data = resp.json()
        _cached_uv = round(data['current']['uv_index'])
        _last_fetch = now
    except Exception as e:
        print(f"UV fetch error: {e}")
    return _cached_uv
