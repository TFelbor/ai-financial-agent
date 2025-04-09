import numpy as np
from collections import Counter

class ForensicAnalyzer:
    def __init__(self):
        self.benford_reference = {
            1: 0.301, 2: 0.176, 3: 0.125, 4: 0.097, 
            5: 0.079, 6: 0.067, 7: 0.058, 8: 0.051, 9: 0.046
        }

    def benford_analysis(self, financial_data):
        """Applies Benford's Law analysis to financial statements"""
        first_digits = [int(str(abs(float(x)))[0]) for x in financial_data if float(x) != 0]
        digit_counts = Counter(first_digits)
        total = len(first_digits)
        
        observed_dist = {d: count/total for d, count in digit_counts.items()}
        chi_square = sum(
            ((observed_dist.get(d, 0) - expected)**2) / expected 
            for d, expected in self.benford_reference.items()
        )
        
        return {
            'observed_distribution': observed_dist,
            'expected_distribution': self.benford_reference,
            'chi_square_stat': chi_square,
            'suspicious_threshold': 15.51  # 95% confidence level with 8 degrees of freedom
        }

    def detect_anomalies(self, time_series_data, window=20):
        """Detects anomalies in financial time series using rolling statistics"""
        rolling_mean = np.mean(time_series_data)
        rolling_std = np.std(time_series_data)
        z_scores = (time_series_data - rolling_mean) / rolling_std
        
        return {
            'anomalies': np.where(abs(z_scores) > 3)[0],  # 3 sigma threshold
            'z_scores': z_scores,
            'severity': abs(z_scores)
        }