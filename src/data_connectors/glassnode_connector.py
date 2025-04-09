import requests
import os
from datetime import datetime
from src.config.config import Config
from cachetools import cached, TTLCache

class GlassnodeConnector:
    BASE_URL = "https://api.glassnode.com/v1/metrics"
    
    def __init__(self):
        self.api_key = Config.GLASSNODE_API
        self.cache = TTLCache(maxsize=100, ttl=3600)
    
    @cached(cache)
    def get_metric(self, metric: str, asset: str = "BTC", frequency: str = "24h"):
        endpoint = f"{self.BASE_URL}/{metric}"
        params = {
            "a": asset,
            "i": frequency,
            "api_key": self.api_key
        }
        response = requests.get(endpoint, params=params)
        return response.json()
    
    def get_miner_flows(self):
        return self.get_metric("mining/flow_sum")
    
    def get_exchange_balances(self):
        return self.get_metric("distribution/balance_exchanges")
