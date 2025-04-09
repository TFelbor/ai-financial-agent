import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
import sys

# Import seaborn and set style
try:
    print("Importing seaborn...", file=sys.stderr)
    import seaborn as sns
    sns.set_theme(style="darkgrid")  # Modern way to set seaborn style
    print("Seaborn style set successfully", file=sys.stderr)
except Exception as e:
    print(f"Warning: Could not set seaborn style: {e}", file=sys.stderr)
    # Fallback to a basic matplotlib style
    plt.style.use('default')

# Update rcParams for consistent styling
plt.rcParams.update({
    'axes.grid': True,
    'grid.alpha': 0.3,
    'axes.titlepad': 20,
    'font.size': 10,
    'figure.figsize': (16, 12)
})

class FinancialVisualizer:
    def __init__(self):
        self.colors = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'highlight': '#d62728'
        }
    
    def create_equity_report(self, ticker, fundamentals, price_data):
        fig = plt.figure(figsize=self.fig_size, tight_layout=True)
        gs = fig.add_gridspec(3, 3)
        
        # Price Chart
        ax1 = fig.add_subplot(gs[0, :])
        ax1.plot(price_data.index, price_data['Close'], 
                color=self.colors['primary'], linewidth=2)
        ax1.set_title(f'{ticker} Price History', fontweight='bold')
        
        # Volume Subplot
        ax1v = ax1.twinx()
        ax1v.bar(price_data.index, price_data['Volume'], 
                alpha=0.3, color=self.colors['secondary'])
        ax1v.yaxis.set_major_formatter(
            FuncFormatter(lambda x, pos: f'{x/1e6:.1f}M'))
        
        # Fundamentals Heatmap
        ax2 = fig.add_subplot(gs[1:, 1:])
        fundamentals.T.plot(kind='bar', ax=ax2, width=0.8,
                          color=[self.colors['primary'], 
                                self.colors['secondary']])
        ax2.xaxis.set_major_locator(mdates.YearLocator())
        
        # Risk Metrics
        ax3 = fig.add_subplot(gs[1:, 0])
        # Add risk calculations here
        
        return fig
