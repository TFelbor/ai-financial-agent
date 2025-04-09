import numpy as np
from scipy.optimize import minimize
import pandas as pd

class RiskEngine:
    def __init__(self):
        self.confidence_level = 0.95
        
    def calculate_cvar(self, returns, weights=None):
        """Calculate Conditional Value at Risk"""
        if weights is None:
            weights = np.ones(len(returns)) / len(returns)
            
        portfolio_returns = np.dot(returns, weights)
        var = np.percentile(portfolio_returns, (1 - self.confidence_level) * 100)
        cvar = np.mean(portfolio_returns[portfolio_returns <= var])
        
        return {
            'VaR': var,
            'CVaR': cvar,
            'confidence_level': self.confidence_level
        }
    
    def optimize_portfolio(self, returns, target_return=None):
        """Portfolio optimization using CVaR as risk measure"""
        n_assets = returns.shape[1]
        
        def objective(weights):
            return -self.calculate_cvar(returns, weights)['CVaR']
        
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}  # weights sum to 1
        ]
        
        if target_return is not None:
            constraints.append({
                'type': 'eq',
                'fun': lambda x: np.sum(returns.mean() * x) - target_return
            })
            
        bounds = tuple((0, 1) for _ in range(n_assets))
        
        result = minimize(
            objective,
            x0=np.ones(n_assets) / n_assets,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        return {
            'optimal_weights': result.x,
            'optimized_cvar': -result.fun,
            'success': result.success,
            'message': result.message
        }
