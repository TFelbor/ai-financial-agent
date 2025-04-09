# API Specifications

## REST API Endpoints

### `GET /api/analyze/{ticker}`
Analyzes a single security/crypto asset

**Parameters:**
```code
    | Name   | Type   | Required | Description               
    ---------+--------+----------+---------------------------------------
    | ticker | string | Yes      | Asset symbol (e.g. `AAPL`, `BTC-USD`) 
    ---------+--------+----------+---------------------------------------
```
**Response:**
```json
{
  "metadata": {
    "ticker": "AAPL",
    "timestamp": "2025-03-21T14:30:00Z",
    "data_source": "Yahoo Finance"
  },
  "valuation": {
    "dcf_mean": 185.72,
    "discount_rate": 0.072,
    "sensitivity_analysis": {
      "bull_case": 210.40,
      "base_case": 185.72,
      "bear_case": 162.35
    }
  },
  "risk_metrics": {
    "beta": 1.28,
    "sharpe_ratio": 0.92,
    "max_drawdown": -0.243
  }
}
```

```code
GET /api/compare
```
**Compare multiple assets**
*Parameters:*
```code
?tickers=AAPL,MSFT,GOOG&metrics=pe,ev_ebitda,volatility
```

*Response:*
```json
{
  "results": [
    {
      "ticker": "AAPL",
      "pe": 28.45,
      "ev_ebitda": 22.17,
      "volatility": 0.312
    }
  ],
  "normalized_scores": {
    "value_rank": ["MSFT", "GOOG", "AAPL"],
    "risk_rank": ["GOOG", "AAPL", "MSFT"]
  }
}
```

**WebSocket API**
```code
    /ws/alerts
```

**Real-time market alert stream**
*Subscription Message:*
```json
{
  "action": "subscribe",
  "channels": ["volatility", "liquidity"]
}
```

*Data Message:*
```json
{
  "event_id": "alert_98237",
  "timestamp": "2025-03-21T14:35:12Z",
  "alert_type": "volume_spike",
  "severity": "high",
  "ticker": "TSLA",
  "metrics": {
    "current_volume": 45218425,
    "avg_volume": 28572194,
    "z_score": 5.83
  }
}
```

**Python Client Example**
```python
    import requests

    class FinancialAPI:
        BASE_URL = "http://localhost:8000/api"

        def __init__(self, api_key):
            self.session = requests.Session()
            self.session.headers.update({"X-API-KEY": api_key})

        def analyze(self, ticker):
            response = self.session.get(f"{self.BASE_URL}/analyze/{ticker}")
            return self._handle_response(response)
        
        def _handle_response(self, response):
            if response.status_code == 429:
                print("Rate limit exceeded - adding delay")
                time.sleep(60)
            return response.json()
```

**Error Responses**
Code    |	Message	Resolution
--------+------------------------------------------------
400	    |   Invalid ticker format	Use uppercase symbols (AAPL)
--------+------------------------------------------------
429	    |   Rate limit exceeded	Implement exponential backoff
--------+------------------------------------------------
503	    |   Data source unavailable	Retry with ?fallback=true
--------+------------------------------------------------

## Key Features Documentation
- Rate Limiting: 100 requests/minute (per API key)
- Smart Caching: Responses include Cache-Control headers
- Bulk Requests: Use comma-separated tickers in batch endpoints
- Field Selection: Control response size with ?fields=pe,volume
