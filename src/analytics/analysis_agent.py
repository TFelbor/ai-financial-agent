from typing import Dict, Optional
import pandas as pd
import plotly.graph_objects as go
from src.reporting.analysis_report import AnalysisReport, AnalysisSection

class FinancialAnalysisAgent:
    def __init__(self):
        self.report = None
        
    async def analyze_security(self, ticker: str) -> AnalysisReport:
        """Perform comprehensive security analysis"""
        self.report = AnalysisReport(ticker)
        
        try:
            # Valuation Analysis
            valuation_data = await self._perform_valuation_analysis(ticker)
            self.report.add_section(valuation_data)
            
            # Technical Analysis
            technical_data = await self._perform_technical_analysis(ticker)
            self.report.add_section(technical_data)
            
            # Risk Analysis
            risk_data = await self._perform_risk_analysis(ticker)
            self.report.add_section(risk_data)
            
            # Forensic Analysis
            forensic_data = await self._perform_forensic_analysis(ticker)
            self.report.add_section(forensic_data)
            
        except Exception as e:
            print(f"Error during analysis: {str(e)}")
            
        return self.report
    
    async def _perform_valuation_analysis(self, ticker: str) -> AnalysisSection:
        try:
            # Attempt to get fundamental data
            fundamentals = await self._fetch_fundamentals(ticker)
            
            dcf_results = self.quant_analyzer.monte_carlo_dcf(
                fundamentals['cash_flows'],
                fundamentals['growth_rates'],
                fundamentals['beta']
            )
            
            charts = [
                self._create_valuation_distribution_chart(dcf_results),
                self._create_sensitivity_analysis_chart(dcf_results)
            ]
            
            return AnalysisSection(
                title="Valuation Analysis",
                summary=self._generate_valuation_summary(dcf_results, fundamentals),
                details={
                    "Estimated Fair Value": dcf_results['mean_valuation'],
                    "Confidence Interval": f"${dcf_results['confidence_interval'][0]:,.2f} - ${dcf_results['confidence_interval'][1]:,.2f}",
                    "Current Price": fundamentals['current_price'],
                    "Upside/Downside": f"{((dcf_results['mean_valuation'] / fundamentals['current_price']) - 1) * 100:.1f}%"
                },
                charts=charts,
                recommendations=self._generate_valuation_recommendations(dcf_results, fundamentals),
                educational_notes=[
                    "DCF valuation estimates the intrinsic value by discounting future cash flows",
                    "Monte Carlo simulation accounts for uncertainty in future growth rates",
                    "A wide confidence interval suggests higher uncertainty in the valuation"
                ]
            )
            
        except Exception as e:
            self.report.mark_unavailable(
                "Fundamental Data",
                f"Unable to perform valuation analysis: {str(e)}"
            )
            return self._generate_empty_section("Valuation Analysis")
    
    async def _perform_technical_analysis(self, ticker: str) -> AnalysisSection:
        try:
            price_data = await self._fetch_price_data(ticker)
            
            technical_indicators = self._calculate_technical_indicators(price_data)
            
            charts = [
                self._create_technical_analysis_chart(price_data),
                self._create_momentum_indicators_chart(technical_indicators)
            ]
            
            return AnalysisSection(
                title="Technical Analysis",
                summary=self._generate_technical_summary(technical_indicators),
                details={
                    "Trend Direction": technical_indicators['trend'],
                    "RSI": technical_indicators['rsi'],
                    "MACD Signal": technical_indicators['macd_signal'],
                    "Volume Trend": technical_indicators['volume_trend']
                },
                charts=charts,
                recommendations=self._generate_technical_recommendations(technical_indicators),
                educational_notes=[
                    "Technical analysis studies price patterns and market momentum",
                    "RSI above 70 suggests overbought conditions, below 30 suggests oversold",
                    "MACD crossovers can signal potential trend changes"
                ]
            )
            
        except Exception as e:
            self.report.mark_unavailable(
                "Price Data",
                f"Unable to perform technical analysis: {str(e)}"
            )
            return self._generate_empty_section("Technical Analysis")
    
    def _generate_empty_section(self, title: str) -> AnalysisSection:
        return AnalysisSection(
            title=title,
            summary="Analysis not available",
            details={},
            charts=[],
            recommendations=[],
            educational_notes=[]
        )
    
    def _create_valuation_distribution_chart(self, dcf_results: Dict) -> go.Figure:
        """Create distribution chart of DCF valuations"""
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=dcf_results['simulations'],
            nbinsx=50,
            name="Valuation Distribution"
        ))
        fig.update_layout(
            title="Distribution of Possible Valuations",
            xaxis_title="Valuation ($)",
            yaxis_title="Frequency",
            showlegend=True
        )
        return fig
    
    def _generate_valuation_summary(self, dcf_results: Dict, fundamentals: Dict) -> str:
        """Generate natural language summary of valuation analysis"""
        current_price = fundamentals['current_price']
        fair_value = dcf_results['mean_valuation']
        
        if fair_value > current_price * 1.2:
            sentiment = "significantly undervalued"
        elif fair_value > current_price * 1.05:
            sentiment = "slightly undervalued"
        elif fair_value < current_price * 0.8:
            sentiment = "significantly overvalued"
        elif fair_value < current_price * 0.95:
            sentiment = "slightly overvalued"
        else:
            sentiment = "fairly valued"
            
        return f"""
        Based on our DCF analysis, {self.ticker} appears to be {sentiment} at current prices. 
        The estimated fair value of ${fair_value:,.2f} represents a 
        {((fair_value/current_price - 1) * 100):.1f}% difference from the current market price.
        Our confidence interval suggests a range of possible values between 
        ${dcf_results['confidence_interval'][0]:,.2f} and ${dcf_results['confidence_interval'][1]:,.2f}.
        """