import requests
from typing import Any, Dict, Optional


class HTTPClientError(Exception):
    pass

class HTTPClient:
    def __init__(self, timeout: float = 10.0):
        self.timeout = timeout
        self.session = requests.Session()

    def get(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout as err:
            raise HTTPClientError(f"Request timed out after {self.timeout}s for URL '{url}'") from err
        except requests.exceptions.HTTPError as err:
            raise HTTPClientError(f"HTTP {err.response.status_code} error fetching '{url}'") from err
        except requests.exceptions.RequestException as err:
            raise HTTPClientError(f"Network error executing request to '{url}': {err}") from err
