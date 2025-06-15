import yfinance as yf
from datetime import datetime
from app.services.providers.base import BaseProvider

class YFinanceProvider(BaseProvider):
    def get_price(self, symbol: str) -> dict:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d", interval="1m")

        if data.empty:
            raise RuntimeError(f"No data found for symbol: {symbol}")

        latest_row = data.iloc[-1]

        return {
            "symbol": symbol,
            "price": float(latest_row["Open"]),
            "timestamp": latest_row.name.to_pydatetime(),
            "provider": "yfinance"
        }
