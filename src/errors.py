from datetime import datetime
from typing import Any, Dict, Optional

class AnalysisError(Exception):
    """Base exception for all analysis-related errors"""
    def __init__(self, message: str, ticker: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.ticker = ticker
        self.details = details or {}
        self.timestamp = datetime.now().isoformat()
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'error': self.message,
            'ticker': self.ticker,
            'timestamp': self.timestamp,
            'details': self.details
        }

class ValidationError(AnalysisError):
    """Raised when input validation fails"""
    pass

class DataSourceError(AnalysisError):
    """Raised when data fetching fails"""
    pass

class CalculationError(AnalysisError):
    """Raised when financial calculations fail"""
    pass