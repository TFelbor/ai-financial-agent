# Troubleshooting Guide

## Installation Issues

### TA-Lib Compilation Errors
**MacOS**
```bash
    brew install ta-lib
    export TA_LIBRARY_PATH=/usr/local/opt/ta-lib/lib
    export TA_INCLUDE_PATH=/usr/local/opt/ta-lib/include
    pip install --no-cache-dir ta-lib
```
*Memory Errors during Backtesting*
1. Enable chunk processing:
```python
    def chunk_processing(data, chunk_size=1000000):
        for i in range(0, len(data), chunk_size):
            yield data[i:i + chunk_size]
```

2. Set os.environ['TF_GPU_ALLOCATOR'] = 'cuda_malloc_async' *for GPU users*

## API Error Handling

### Yahoo Finance 429 Errors
```python
    from tenacity import retry, stop_after_attempt, wait_exponential

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=10))
    def fetch_yahoo_data(ticker):
        return yf.Ticker(ticker).history(period="max")
```

## Data Quality Issues
### Handling Missing Crypto Data
```python
    def clean_crypto_data(df):
        return df.replace(0, np.nan).interpolate().fillna(method='ffill')
```