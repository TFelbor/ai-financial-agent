import yfinance as yf
import pandas as pd
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class YahooConnector:
    def __init__(self):
        self.cache = {}
        
    def is_crypto(self, ticker: str) -> bool:
        """Check if the ticker is a cryptocurrency"""
        return ticker.upper().endswith('-USD') or ticker.upper() in ['BTC', 'ETH']
        
    def get_fundamentals(self, ticker: str) -> dict:
        """Get fundamental data for a ticker"""
        try:
            # For cryptocurrencies, return a simplified structure
            if self.is_crypto(ticker):
                ticker = ticker.upper()
                if not ticker.endswith('-USD'):
                    ticker = f"{ticker}-USD"
                    
                crypto = yf.Ticker(ticker)
                market_cap = crypto.info.get('marketCap', 0)
                
                return {
                    'raw_data': {
                        'balance_sheet': pd.DataFrame({
                            'Total Assets': [market_cap],
                            'Market Cap': [market_cap]
                        })
                    }
                }
            
            # For stocks, get full fundamentals
            stock = yf.Ticker(ticker)
            return {
                'raw_data': {
                    'balance_sheet': stock.balance_sheet,
                    'cash_flow': stock.cashflow,
                    'income_stmt': stock.income_stmt
                }
            }
            
        except Exception as e:
            logger.error(f"Error fetching fundamentals for {ticker}: {str(e)}")
            raise
            
    def get_historical_data(self, ticker: str, period: str = "1y") -> pd.DataFrame:
        """Get historical price data"""
        try:
            # Adjust ticker format for crypto
            if self.is_crypto(ticker):
                ticker = ticker.upper()
                if not ticker.endswith('-USD'):
                    ticker = f"{ticker}-USD"
            
            data = yf.download(ticker, period=period)
            if data.empty:
                raise ValueError(f"No data available for {ticker}")
            return data
            
        except Exception as e:
            logger.error(f"Error fetching historical data for {ticker}: {str(e)}")
            raise
