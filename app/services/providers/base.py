from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @abstractmethod
    def get_price(self, symbol: str) -> dict:
        """
        Return a dict with price data:
        {
            "symbol": "AAPL",
            "price": 150.25,
            "timestamp": "2024-06-14T10:30:00Z",
            "provider": "alpha_vantage"
        }
        """
        pass
