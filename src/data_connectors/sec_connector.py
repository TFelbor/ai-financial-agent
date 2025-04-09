import aiohttp
import asyncio
from pathlib import Path

class AsyncSECConnector:
    async def download_filings(self, ticker: str, filing_type: str = "10-K", years: int = 3):
        base_url = "https://www.sec.gov/Archives/edgar/data"
        async with aiohttp.ClientSession() as session:
            tasks = []
            for year in range(2023, 2023 - years, -1):
                url = f"{base_url}/{ticker}/{filing_type}_{year}.json"
                tasks.append(self._download_file(session, url, f"{ticker}_{filing_type}_{year}.json"))
            await asyncio.gather(*tasks)

    async def _download_file(self, session, url, filename):
        async with session.get(url) as response:
            content = await response.read()
            Path(f"data/sec_filings/{filename}").write_bytes(content)
