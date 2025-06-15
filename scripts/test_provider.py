from app.services.providers.yfinance_provider import YFinanceProvider

provider = YFinanceProvider()
print(provider.get_price("AAPL"))