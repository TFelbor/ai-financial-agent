from multiprocessing import Pool
import numpy as np
import pandas as pd
from numpy import nan
import logging

logger = logging.getLogger(__name__)

class ValuationEngine:
    def __init__(self):
        self.risk_free_rate = 0.03  # 3% risk-free rate
        self.market_risk_premium = 0.06  # 6% market risk premium
        
    def _calculate_npv(self, cash_flows, discount_rate):
        """Calculate NPV manually since numpy.npv is not available"""
        return sum(cf / (1 + discount_rate)**i for i, cf in enumerate(cash_flows))
        
    def monte_carlo_dcf(self, cash_flows: pd.Series, n_simulations: int = 1000):
        """
        Perform Monte Carlo DCF valuation
        """
        try:
            # Convert to numpy array and drop any NaN values
            historical_fcf = cash_flows.dropna().values
            
            if len(historical_fcf) < 2:
                raise ValueError("Insufficient cash flow data for analysis")
            
            # Calculate growth rates
            growth_rates = np.diff(historical_fcf) / historical_fcf[:-1]
            mu = growth_rates.mean()
            sigma = growth_rates.std()
            
            # Project future cash flows
            latest_fcf = historical_fcf[-1]
            years = 5
            discount_rate = self.risk_free_rate + self.market_risk_premium
            
            npvs = []
            for _ in range(n_simulations):
                # Generate random growth rates
                sim_growth_rates = np.random.normal(mu, sigma, years)
                
                # Calculate future cash flows
                future_fcf = latest_fcf
                sim_cash_flows = [future_fcf]
                for g in sim_growth_rates:
                    future_fcf *= (1 + g)
                    sim_cash_flows.append(future_fcf)
                
                # Terminal value (Gordon Growth Model)
                terminal_growth = 0.02  # 2% perpetual growth
                terminal_value = sim_cash_flows[-1] * (1 + terminal_growth) / (discount_rate - terminal_growth)
                sim_cash_flows[-1] += terminal_value
                
                # Calculate NPV
                npv = self._calculate_npv(sim_cash_flows, discount_rate)
                npvs.append(npv)
            
            return self._analyze_results(npvs)
            
        except Exception as e:
            logger.error(f"Error in Monte Carlo DCF: {str(e)}")
            raise
    
    def _analyze_results(self, npvs):
        """Analyze Monte Carlo simulation results"""
        return {
            'mean': float(np.mean(npvs)),
            'std': float(np.std(npvs)),
            'ci_lower': float(np.percentile(npvs, 2.5)),
            'ci_upper': float(np.percentile(npvs, 97.5)),
            'median': float(np.median(npvs))
        }

class ParallelValuationEngine(ValuationEngine):
    def _run_single_simulation(self, args):
        mu, sigma, years = args
        trial = np.random.normal(mu, sigma, years)
        return np.npv(0.1, trial)

    def monte_carlo_dcf(self, cash_flows: pd.Series, years: int = 5, simulations: int = 10000):
        mu, sigma = cash_flows.mean(), cash_flows.std()
        with Pool() as pool:
            npvs = pool.map(
                self._run_single_simulation,
                [(mu, sigma, years)] * simulations
            )
        return self._analyze_results(npvs)
