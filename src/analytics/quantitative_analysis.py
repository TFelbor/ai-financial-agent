import numpy as np
from scipy.stats import norm

class QuantitativeAnalysis:
    def __init__(self):
        self.risk_free_rate = 0.035  # Updated periodically
        self.market_risk_premium = 0.06
        
    def monte_carlo_dcf(self, cash_flows, growth_rates, beta, simulations=10000):
        """Monte Carlo simulation for DCF valuation"""
        terminal_multiple = 15  # Industry average P/E
        
        # Generate random growth scenarios
        growth_scenarios = np.random.normal(
            loc=np.mean(growth_rates),
            scale=np.std(growth_rates),
            size=(simulations, len(cash_flows))
        )
        
        # Calculate cost of equity using CAPM
        cost_of_equity = self.risk_free_rate + beta * self.market_risk_premium
        
        valuations = []
        for scenario in growth_scenarios:
            projected_cash_flows = cash_flows * (1 + scenario)
            terminal_value = (projected_cash_flows[-1] * (1 + scenario[-1])) * terminal_multiple
            
            # Discount cash flows
            discount_factors = 1 / (1 + cost_of_equity) ** np.arange(1, len(cash_flows) + 1)
            present_value = sum(projected_cash_flows * discount_factors)
            terminal_present_value = terminal_value * discount_factors[-1]
            
            valuations.append(present_value + terminal_present_value)
            
        return {
            'mean_valuation': np.mean(valuations),
            'std_valuation': np.std(valuations),
            'confidence_interval': norm.interval(0.95, np.mean(valuations), np.std(valuations)),
            'scenarios': {
                'bull_case': np.percentile(valuations, 90),
                'base_case': np.percentile(valuations, 50),
                'bear_case': np.percentile(valuations, 10)
            }
        }