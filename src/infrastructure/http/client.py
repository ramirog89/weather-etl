import requests
from typing import Any, Dict, Optional


class HTTPClient:
    def __init__(self, timeout: float = 10.0):
        self.timeout = timeout
        self.session = requests.Session()

    def get(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as err:
            raise RuntimeError(f"HTTP request failed: {err}") from err
