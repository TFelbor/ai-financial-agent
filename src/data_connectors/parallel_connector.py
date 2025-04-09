import concurrent.futures
from typing import List, Dict

class ParallelDataFetcher:
    def __init__(self):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

    def fetch_multiple_tickers(self, tickers: List[str]) -> Dict[str, Dict]:
        with self.executor:
            future_to_ticker = {
                self.executor.submit(YahooConnector().get_historical, ticker): ticker
                for ticker in tickers
            }
            results = {}
            for future in concurrent.futures.as_completed(future_to_ticker):
                ticker = future_to_ticker[future]
                try:
                    results[ticker] = future.result()
                except Exception as e:
                    print(f"Error fetching {ticker}: {e}")
            return results
