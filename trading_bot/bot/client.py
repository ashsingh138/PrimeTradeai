import requests
import time
import hmac
import hashlib
from urllib.parse import urlencode
from .logging_config import logger

class BinanceAPIError(Exception):
    pass

class BinanceFuturesClient:
    BASE_URL = "https://testnet.binancefuture.com"

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded"
        })

    def _generate_signature(self, params: dict) -> str:
        query_string = urlencode(params)
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def dispatch_request(self, method: str, endpoint: str, params: dict = None):
        if params is None:
            params = {}
            
        params['timestamp'] = int(time.time() * 1000)
        params['signature'] = self._generate_signature(params)

        url = f"{self.BASE_URL}{endpoint}"
        
        logger.debug(f"Sending {method} request to {url} with params: {params}")
        
        try:
            response = self.session.request(method, url, params=params)
            response.raise_for_status() # Raise exception for HTTP errors (4xx, 5xx)
            data = response.json()
            
            # Catch Binance specific application errors
            if 'code' in data and data['code'] < 0:
                raise BinanceAPIError(f"Binance Error {data['code']}: {data['msg']}")
                
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error occurred: {str(e)}")
            if response is not None and response.text:
                logger.error(f"Response content: {response.text}")
            raise BinanceAPIError(f"Network/HTTP Error: {str(e)}")