from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
import asyncio

from src.analytics.quantitative_analysis import QuantitativeAnalysis
from src.analytics.forensic_analyzer import ForensicAnalyzer
from src.analytics.risk_engine import RiskEngine
from ..errors import AnalysisError, DataSourceError, ValidationError
from ..cache import analysis_cache

app = FastAPI(title="AI Financial Analysis Agent")

quant_analyzer = QuantitativeAnalysis()
forensic_analyzer = ForensicAnalyzer()
risk_engine = RiskEngine()

class AnalysisRequest(BaseModel):
    ticker: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    analysis_type: List[str] = ['all']

@app.get("/api/analyze/{ticker}")
async def analyze_stock_endpoint(
    ticker: str,
    refresh_cache: bool = Query(False, description="Force refresh cached data")
):
    try:
        # Clear cache if requested
        if refresh_cache:
            analysis_cache.clear_expired()
        
        result = await analyze_stock(ticker)
        
        if 'error' in result:
            raise HTTPException(
                status_code=400 if isinstance(result.get('error'), ValidationError) else 500,
                detail=result
            )
            
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"API error for {ticker}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={"error": str(e), "ticker": ticker}
        )

@app.get("/api/analyze/batch/{tickers}")
async def analyze_stocks_batch(tickers: str):
    """Batch analysis endpoint for multiple tickers"""
    ticker_list = [t.strip() for t in tickers.split(',')]
    
    # Validate input
    if len(ticker_list) > 10:  # Limit batch size
        raise HTTPException(
            status_code=400,
            detail={"error": "Maximum 10 tickers allowed per batch request"}
        )
    
    # Process all tickers concurrently
    tasks = [analyze_stock(ticker) for ticker in ticker_list]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    return {
        "batch_results": {
            ticker: result for ticker, result in zip(ticker_list, results)
        }
    }

async def fetch_market_data(ticker: str):
    """Fetch required market data for analysis"""
    # Implementation depends on data source
    pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
