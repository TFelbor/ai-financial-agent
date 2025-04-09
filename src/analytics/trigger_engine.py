import asyncio
from datetime import datetime
import numpy as np

class MarketTrigger:
    def __init__(self):
        self.active_triggers = {}
        self.running = False
        
    async def monitor_price(self, ticker, threshold, condition, callback):
        """Monitor price movements and trigger alerts"""
        while self.running:
            try:
                current_price = await self._fetch_latest_price(ticker)
                if self._evaluate_condition(current_price, threshold, condition):
                    await callback({
                        'ticker': ticker,
                        'price': current_price,
                        'threshold': threshold,
                        'condition': condition,
                        'timestamp': datetime.now().isoformat()
                    })
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                print(f"Error monitoring {ticker}: {str(e)}")
                
    def _evaluate_condition(self, price, threshold, condition):
        if condition == 'above':
            return price > threshold
        elif condition == 'below':
            return price < threshold
        elif condition == 'percent_change':
            return abs(self.last_price[ticker] - price) / self.last_price[ticker] > threshold
            
    async def _fetch_latest_price(self, ticker):
        """Fetch real-time price data"""
        # Implementation depends on data source (e.g., Yahoo Finance, Alpha Vantage)
        pass
        
    def add_trigger(self, ticker, threshold, condition, callback):
        """Add new price trigger"""
        if ticker not in self.active_triggers:
            self.active_triggers[ticker] = []
        self.active_triggers[ticker].append({
            'threshold': threshold,
            'condition': condition,
            'callback': callback
        })
        
    def start(self):
        """Start monitoring all triggers"""
        self.running = True
        loop = asyncio.get_event_loop()
        for ticker, triggers in self.active_triggers.items():
            for trigger in triggers:
                loop.create_task(
                    self.monitor_price(
                        ticker,
                        trigger['threshold'],
                        trigger['condition'],
                        trigger['callback']
                    )
                )
        
    def stop(self):
        """Stop all monitoring"""
        self.running = False
