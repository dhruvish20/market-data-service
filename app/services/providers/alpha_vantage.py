import os
import requests
from datetime import datetime
from app.services.providers.base import BaseProvider

class AlphaVantageProvider(BaseProvider):
    def __init__(self):
        self.api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        self.base_url = "https://www.alphavantage.co/query"

    def get_price(self, symbol: str) -> dict:
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            # "interval": "1min",
            "apikey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()

        # Get the latest timestamp from response
        try:
            time_series = data["Time Series (1min)"]
            latest_timestamp = sorted(time_series.keys())[-1]
            latest_data = time_series[latest_timestamp]
            return {
                "symbol": symbol,
                "price": float(latest_data["1. open"]),
                "timestamp": datetime.fromisoformat(latest_timestamp),
                "provider": "alpha_vantage"
            }
        except Exception as e:
            raise RuntimeError(f"Error parsing Alpha Vantage data: {e}")
