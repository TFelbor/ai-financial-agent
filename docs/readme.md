# AI Financial Analysis Agent

![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Dashboard Preview
<img src="data/outputs/website_preview_1.png" width="300" />
![Preview 1](data/outputs/website_preview_1)
![Preview_2](data/outputs/website_preview_2)
![Preview_3](data/outputs/website_preview_3)

An advanced quantitative analysis platform combining machine learning, forensic accounting, and real-time market monitoring for stocks and cryptocurrencies.

## Features

- **Multi-Asset Coverage**: Analyze traditional securities & cryptoassets
- **Automated Alerts**: Trigger-based notifications for market anomalies (development phase)
- **Forensic Accounting**: Benford's Law analysis for financial statements
- **Quantitative Models**: 
  - Monte Carlo DCF valuations
  - Risk-adjusted portfolio optimization
- **Real-Time Dashboard**: FastAPI-based web interface with interactive visuals

## Installation

### Prerequisites

1. **MacOS**: Install Homebrew (if not installed):
```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Install TA-Lib System Library:
```bash 
    brew install ta-lib
```

### Setup

1. Clone the repository:
```bash
    git clone https://github.com/yourusername/ai-financial-agent.git
    cd ai-financial-agent
```

2. Create and activate virtual environment:
```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate    # Windows
```
3. Install dependencies:
```bash
    pip install -r requirements.txt
```

4. Set up API keys:
```bash
    cp config/secrets.env.example config/secrets.env
```
  -> Edit config/secrets.env with your:
  - Yahoo Finance API token
  - Glassnode API key
  - SEC EDGAR API key

## Project Structure

```code
    financial_agent/
    ├── data/               # Cached data and outputs
    ├── static/             # CSS/JS assets
    ├── templates/          # HTML templates
    ├── src/
    │   ├── analytics/      # Core analysis engines
    │   ├── api/            # FastAPI endpoints
    │   ├── config/         # Configuration
    │   └── data_connectors # Market data sources
    └── tests/              # Unit tests
```
    
## Usage
    
### Running the Dashboard

For development (with auto-reload):
```bash
    python -m src.api.run
```
    -> Access the web interface at: http://localhost:8000

For production:
```bash
    uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Command Line Analysis
```bash
    python -m src.main --ticker AAPL
```

### Scheduled Tasks
To run background monitoring:
```python
    from src.analytics.trigger_engine import MarketTrigger
    trigger = MarketTrigger()
    trigger.start()
```

## Key Components

### Data Connectors
```
--------------------+-----------------------------------
Module              | Description
--------------------+-----------------------------------
MarketConnector     | Real-time price updates
--------------------+-----------------------------------
YahooConnector      | Stock fundamentals/price data
--------------------+-----------------------------------
GlassnodeConnector  | Crypto on-chain metrics
--------------------+-----------------------------------
SECConnector        | Automated 10-K/Q filings retrieval
--------------------+-----------------------------------
```

### Analytics Modules
```
Engine                  | Functionality
------------------------+--------------------------------
QuantitativeAnalysis    | DCF, relative valuation models
------------------------+--------------------------------
ForensicAnalyzer        | Accounting anomaly detection
------------------------+--------------------------------
RiskEngine              | CVaR, portfolio optimization
------------------------+--------------------------------
```

## Documentation

- API Reference          -> api.md
- Analysis Methodology   -> methodology.md
- Troubleshooting        -> troubleshooting.md

Example Reports
Equity Analysis Sample
Crypto Dashboard

License
MIT License. See LICENSE for details.
