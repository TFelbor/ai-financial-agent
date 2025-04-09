from dataclasses import dataclass
from typing import Dict, List, Optional
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

@dataclass
class AnalysisSection:
    title: str
    summary: str
    details: Dict
    charts: List[go.Figure]
    recommendations: List[str]
    educational_notes: List[str]

class AnalysisReport:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.sections = []
        self.unavailable_data = {}
        
    def add_section(self, section: AnalysisSection):
        self.sections.append(section)
        
    def mark_unavailable(self, data_type: str, reason: str):
        self.unavailable_data[data_type] = reason
        
    def generate_html(self) -> str:
        """Generate formatted HTML report"""
        html = f"""
        <div class="analysis-report">
            <div class="report-header">
                <h1>{self.ticker} Comprehensive Analysis Report</h1>
                <p class="timestamp">Generated on {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        """
        
        # Add unavailable data warnings if any
        if self.unavailable_data:
            html += '<div class="unavailable-data-section">'
            html += '<h3>⚠️ Data Availability Notes</h3>'
            for data_type, reason in self.unavailable_data.items():
                html += f'<p class="unavailable-item"><strong>{data_type}:</strong> {reason}</p>'
            html += '</div>'
            
        # Add each analysis section
        for section in self.sections:
            html += self._format_section(section)
            
        html += '</div>'
        return html
    
    def _format_section(self, section: AnalysisSection) -> str:
        """Format individual analysis section"""
        html = f"""
        <div class="analysis-section">
            <h2>{section.title}</h2>
            <div class="summary-box">
                <h3>Key Takeaways</h3>
                <p>{section.summary}</p>
            </div>
            
            <div class="details-section">
                <h3>Detailed Analysis</h3>
                {self._format_details(section.details)}
            </div>
        """
        
        # Add charts if any
        if section.charts:
            html += '<div class="charts-section">'
            for chart in section.charts:
                html += chart.to_html(full_html=False)
            html += '</div>'
            
        # Add recommendations
        if section.recommendations:
            html += """
            <div class="recommendations-box">
                <h3>💡 Recommendations</h3>
                <ul>
            """
            for rec in section.recommendations:
                html += f'<li>{rec}</li>'
            html += '</ul></div>'
            
        # Add educational notes
        if section.educational_notes:
            html += """
            <div class="educational-notes">
                <h3>📚 Educational Notes</h3>
                <ul>
            """
            for note in section.educational_notes:
                html += f'<li>{note}</li>'
            html += '</ul></div>'
            
        html += '</div>'
        return html
    
    def _format_details(self, details: Dict) -> str:
        """Format detailed analysis metrics"""
        html = '<div class="metrics-grid">'
        for key, value in details.items():
            if isinstance(value, (int, float)):
                formatted_value = f"{value:,.2f}"
            else:
                formatted_value = str(value)
            
            html += f"""
            <div class="metric-card">
                <h4>{key}</h4>
                <p class="metric-value">{formatted_value}</p>
            </div>
            """
        html += '</div>'
        return html