import logging
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
from .cache import price_cache, analysis_cache
from .errors import AnalysisError, DataSourceError, ValidationError
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, List
import json
import asyncio

logger = logging.getLogger(__name__)

async def get_price_data(ticker: str) -> pd.DataFrame:
    """Fetch historical price data for a ticker"""
    try:
        # Add '-USD' suffix for crypto tickers if not present
        if ticker in ['BTC', 'ETH'] and not ticker.endswith('-USD'):
            ticker = f"{ticker}-USD"

        # Use yfinance to get data
        stock = yf.Ticker(ticker)
        df = stock.history(period='1y')
        
        if df.empty:
            raise DataSourceError(f"No data available for {ticker}")
            
        return df
        
    except Exception as e:
        logger.error(f"Error fetching data for {ticker}: {str(e)}")
        raise DataSourceError(f"Failed to fetch data: {str(e)}")

def calculate_metrics(price_data: pd.DataFrame) -> Dict[str, Any]:
    """Calculate technical indicators and metrics"""
    try:
        # Convert to simple Python types immediately
        latest_price = float(price_data['Close'].iloc[-1])
        latest_volume = int(price_data['Volume'].iloc[-1])
        
        # Calculate SMAs
        sma_50 = None
        sma_200 = None
        if len(price_data) >= 50:
            sma_50 = float(price_data['Close'].rolling(window=50).mean().iloc[-1])
        if len(price_data) >= 200:
            sma_200 = float(price_data['Close'].rolling(window=200).mean().iloc[-1])
        
        # Calculate RSI
        delta = price_data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = float(100 - (100 / (1 + rs.iloc[-1]))) if not pd.isna(rs.iloc[-1]) else None
        
        # Calculate volatility
        returns = price_data['Close'].pct_change()
        volatility = float(returns.std() * np.sqrt(252)) if len(returns) > 1 else None
        
        # Convert returns to list of floats
        returns_list = [float(x) for x in returns.dropna().tolist()]
        
        return {
            'latest_price': latest_price,
            'latest_volume': latest_volume,
            'sma_50': sma_50,
            'sma_200': sma_200,
            'rsi': rsi,
            'volatility': volatility,
            'returns': returns_list
        }
    except Exception as e:
        logger.error(f"Error calculating metrics: {str(e)}")
        return {}

def calculate_market_cap(ticker: str, latest_price: float) -> float:
    """Calculate market cap using yfinance data"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        shares = info.get('sharesOutstanding', 0)
        return float(latest_price * shares) if shares else None
    except:
        return None

async def analyze_stock(ticker: str) -> Dict[str, Any]:
    """Main analysis function"""
    try:
        if not isinstance(ticker, str) or not ticker.strip():
            raise ValidationError("Invalid ticker symbol", ticker)

        # Get price data
        price_data = price_cache.get(ticker)
        if price_data is None:
            price_data = await get_price_data(ticker)
            price_cache.set(ticker, price_data)

        # Calculate metrics
        metrics = calculate_metrics(price_data)
        market_cap = calculate_market_cap(ticker, metrics['latest_price'])

        # Prepare price history
        price_history = {
            'dates': [d.strftime('%Y-%m-%d') for d in price_data.index],
            'prices': [float(p) for p in price_data['Close']],
            'volumes': [int(v) for v in price_data['Volume']]
        }

        result = {
            'ticker': ticker,
            'metrics': {
                'latest_price': metrics['latest_price'],
                'volume': metrics['latest_volume'],
                'market_cap': market_cap if market_cap is not None else 'N/A',
                'technical': {
                    'sma_50': metrics['sma_50'],
                    'sma_200': metrics['sma_200'],
                    'rsi': metrics['rsi'],
                    'volatility': metrics['volatility'],
                    'returns': metrics['returns']
                }
            },
            'price_history': price_history
        }

        # Cache the result
        analysis_cache.set(ticker, result)
        return result

    except Exception as e:
        logger.error(f"Unexpected error analyzing {ticker}: {str(e)}")
        return {'error': str(e), 'ticker': ticker}

# Alias for backward compatibility
analyze_ticker = analyze_stock

async def analyze_multiple_tickers(tickers: List[str]) -> Dict[str, Any]:
    """Analyze multiple tickers concurrently"""
    tasks = [analyze_stock(ticker) for ticker in tickers]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Process results and handle any exceptions
    processed_results = {}
    for ticker, result in zip(tickers, results):
        if isinstance(result, Exception):
            processed_results[ticker] = {
                'error': str(result),
                'ticker': ticker
            }
        else:
            processed_results[ticker] = result
            
    return processed_results

if __name__ == "__main__":
    print("Starting main execution...", file=sys.stderr)
    
    try:
        print("Importing pandas...", file=sys.stderr)
        import pandas as pd
        pd.options.mode.chained_assignment = None
        print("Pandas imported successfully", file=sys.stderr)
        
        print("Importing numpy...", file=sys.stderr)
        import numpy as np
        np.set_printoptions(precision=4)
        print("Numpy imported successfully", file=sys.stderr)
    except Exception as e:
        print(f"Error during imports: {str(e)}", file=sys.stderr)
        sys.exit(1)
    
    # Example usage
    ticker = 'AAPL'
    logger.info(f"Starting analysis for {ticker}")
    result = analyze_stock(ticker)
    
    if result is not None:
        logger.info(f"Valuation Analysis Complete for {ticker}: {result}")
    else:
        logger.error(f"Analysis failed for {ticker}")
