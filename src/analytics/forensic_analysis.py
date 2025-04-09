import numpy as np
import pandas as pd
from typing import Dict

class ForensicAnalyzer:
    def __init__(self):
        self.benford_dist = np.log10(1 + 1/np.arange(1, 10))
    
    def benfords_law_test(self, numbers: pd.Series) -> Dict:
        counts = np.zeros(9)
        valid = numbers.dropna()[numbers > 0]
        
        for num in valid:
            first_digit = int(str(abs(num))[0])  # Get first non-zero digit
            if 1 <= first_digit <= 9:
                counts[first_digit-1] += 1
        
        total = counts.sum()
        observed = counts / total
        chi2 = np.sum((observed - self.benford_dist)**2 / self.benford_dist)
        
        return {
            "expected_distribution": self.benford_dist.tolist(),
            "observed_distribution": observed.tolist(),
            "chi_squared": chi2,
            "anomaly_score": chi2 * 100
        }
    
    def analyze_filing(self, filing_text: str) -> Dict:
        from collections import Counter
        import re
        
        numbers = [float(x) for x in re.findall(r'\d+\.\d+', filing_text)]
        return {
            "benford_test": self.benfords_law_test(pd.Series(numbers)),
            "numbers_count": len(numbers),
            "unique_numbers": len(set(numbers))
        }
