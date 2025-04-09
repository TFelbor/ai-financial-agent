import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class FinancialVisualizer:
    def __init__(self):
        self.figure_size = (12, 8)  # Default figure size
        sns.set_style("whitegrid")
        
    def create_analysis_report(self, ticker: str, price_data: pd.DataFrame, valuation_results: dict):
        """Create a comprehensive analysis visualization"""
        try:
            # Create figure with subplots
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=self.figure_size)
            
            # Price chart
            price_data['Close'].plot(ax=ax1, title=f'{ticker} Price History')
            ax1.set_ylabel('Price')
            
            # Volume chart
            price_data['Volume'].plot(ax=ax2, title=f'{ticker} Volume')
            ax2.set_ylabel('Volume')
            
            # Adjust layout
            plt.tight_layout()
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating visualization: {str(e)}")
            raise