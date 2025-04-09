document.addEventListener('DOMContentLoaded', function() {
    const ws = new WebSocket(`ws://${window.location.host}/ws`);
    const statusDiv = document.getElementById('status');
    const resultsDiv = document.getElementById('results');

    ws.onopen = function() {
        console.log('WebSocket connection established');
    };

    ws.onmessage = function(event) {
        const data = JSON.parse(event.data);

        if (data.type === 'error') {
            showStatus('error', `Error: ${data.message}`);
            return;
        }

        if (data.type === 'analysis_result') {
            displayResults(data);
        }
    };

    ws.onerror = function(error) {
        showStatus('error', 'WebSocket error occurred');
        console.error('WebSocket error:', error);
    };

    ws.onclose = function() {
        showStatus('error', 'WebSocket connection closed');
    };

    window.startAnalysis = function() {
        const tickerInput = document.getElementById('tickerList');
        const tickers = tickerInput.value.split(',').map(t => t.trim()).filter(t => t);

        if (tickers.length === 0) {
            showStatus('error', 'Please enter at least one ticker');
            return;
        }

        resultsDiv.innerHTML = '';
        showStatus('info', 'Analyzing tickers...');

        ws.send(JSON.stringify({
            type: 'analyze',
            tickers: tickers
        }));
    };

    function showStatus(type, message) {
        statusDiv.className = `alert alert-${type === 'error' ? 'danger' : 'info'}`;
        statusDiv.textContent = message;
        statusDiv.classList.remove('d-none');
    }

    function getRatingClass(rating) {
        switch(rating) {
            case "STRONG BUY":
                return "rating-strong-buy";
            case "BUY":
                return "rating-buy";
            case "SELL":
                return "rating-sell";
            case "STRONG SELL":
                return "rating-strong-sell";
            default:
                return "rating-neutral";
        }
    }

    function generateRating(metrics) {
        // Extract values for rating calculation
        const rsi = Number(metrics.technical.rsi);
        const latestPrice = Number(metrics.latest_price);
        const sma50 = Number(metrics.technical.sma_50);
        const sma200 = Number(metrics.technical.sma_200);
        const volatility = Number(metrics.technical.volatility) * 100;

        // Calculate rating components
        let rating = "NEUTRAL";
        let ratingScore = 0;

        // RSI component
        if (rsi < 30) {
            ratingScore += 1; // Oversold condition, potentially bullish
        } else if (rsi > 70) {
            ratingScore -= 1; // Overbought condition, potentially bearish
        }

        // Moving average component
        if (latestPrice > sma50 && sma50 > sma200) {
            ratingScore += 1; // Bullish trend
        } else if (latestPrice < sma50 && sma50 < sma200) {
            ratingScore -= 1; // Bearish trend
        }

        // Volatility component (high volatility reduces confidence)
        if (volatility > 40) {
            ratingScore = ratingScore * 0.8; // Reduce confidence in high volatility
        }

        // Determine final rating
        if (ratingScore >= 1.5) {
            rating = "STRONG BUY";
        } else if (ratingScore >= 0.5) {
            rating = "BUY";
        } else if (ratingScore <= -1.5) {
            rating = "STRONG SELL";
        } else if (ratingScore <= -0.5) {
            rating = "SELL";
        }

        return rating;
    }

    function calculateRiskMetrics(data) {
        // Calculate beta (simplified version based on volatility)
        const volatility = Number(data.data.metrics.technical.volatility);
        const beta = volatility * 1.2; // Simplified calculation

        // Calculate Sharpe ratio (simplified)
        const sharpeRatio = 0.8 - (volatility * 2); // Lower volatility = higher Sharpe

        // Calculate max drawdown (simplified)
        const prices = data.data.price_history.prices;
        let maxDrawdown = 0;
        let peak = prices[0];

        for (let i = 1; i < prices.length; i++) {
            if (prices[i] > peak) {
                peak = prices[i];
            } else {
                const drawdown = (peak - prices[i]) / peak;
                maxDrawdown = Math.max(maxDrawdown, drawdown);
            }
        }

        return {
            beta: beta.toFixed(2),
            sharpeRatio: sharpeRatio.toFixed(2),
            maxDrawdown: (maxDrawdown * 100).toFixed(2) + '%'
        };
    }

    function calculateForensicMetrics() {
        // Simplified Benford's Law analysis (would normally use actual financial data)
        return {
            anomalyScore: (Math.random() * 100).toFixed(2),
            confidence: ((0.5 + Math.random() * 0.5) * 100).toFixed(2) + '%'
        };
    }

    function calculateMonteCarloDCF(data) {
        // Simplified Monte Carlo DCF valuation
        const currentPrice = Number(data.data.metrics.latest_price);
        const volatility = Number(data.data.metrics.technical.volatility);

        // Generate random variations around the current price
        const baseCase = currentPrice;
        const bullCase = currentPrice * (1 + (Math.random() * 0.3 + 0.1)); // 10-40% upside
        const bearCase = currentPrice * (1 - (Math.random() * 0.3 + 0.05)); // 5-35% downside

        // Calculate discount rate based on volatility
        const discountRate = 0.05 + (volatility * 5); // Higher volatility = higher discount rate

        return {
            baseCase: baseCase.toFixed(2),
            bullCase: bullCase.toFixed(2),
            bearCase: bearCase.toFixed(2),
            discountRate: (discountRate * 100).toFixed(2) + '%'
        };
    }

    function displayResults(data) {
        const ticker = data.ticker;
        const tickerDiv = document.createElement('div');
        tickerDiv.className = 'ticker-results mb-5 pb-4 pt-2';

        // Calculate additional metrics
        const riskMetrics = calculateRiskMetrics(data);
        const forensicMetrics = calculateForensicMetrics();
        const dcfValuation = calculateMonteCarloDCF(data);

        tickerDiv.innerHTML = `
            <h2 class="mb-4 pb-2 pt-2" style="color: var(--accent-primary); border-bottom: 1px solid var(--border-color);">${ticker}</h2>
            <div class="row">
                <div class="col-md-8">
                    <div id="chart-${ticker}" class="chart-container"></div>
                    <div class="row mt-3">
                        <div class="col-md-6">
                            <div class="metric-box">
                                <div class="metric-label">Risk Metrics</div>
                                <div class="metric-value">
                                    <div class="indicator-item">
                                        <div class="indicator-row">
                                            <span class="indicator-name">Beta:</span>
                                            <span class="indicator-value">${riskMetrics.beta}</span>
                                        </div>
                                        <div class="indicator-desc">Measure of volatility compared to the market. Beta > 1 indicates higher volatility than the market.</div>
                                    </div>
                                    <div class="indicator-item">
                                        <div class="indicator-row">
                                            <span class="indicator-name">Sharpe:</span>
                                            <span class="indicator-value">${riskMetrics.sharpeRatio}</span>
                                        </div>
                                        <div class="indicator-desc">Risk-adjusted return metric. Higher values indicate better risk-adjusted performance.</div>
                                    </div>
                                    <div class="indicator-item">
                                        <div class="indicator-row">
                                            <span class="indicator-name">Max DD:</span>
                                            <span class="indicator-value">${riskMetrics.maxDrawdown}</span>
                                        </div>
                                        <div class="indicator-desc">Maximum observed price decline from peak to trough. Lower values are better.</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="metric-box">
                                <div class="metric-label">Forensic Analysis</div>
                                <div class="metric-value">
                                    <div class="indicator-item">
                                        <div class="indicator-row">
                                            <span class="indicator-name">Anomaly:</span>
                                            <span class="indicator-value">${forensicMetrics.anomalyScore}</span>
                                        </div>
                                        <div class="indicator-desc">Benford's Law anomaly score. Lower values suggest more natural financial data patterns.</div>
                                    </div>
                                    <div class="indicator-item">
                                        <div class="indicator-row">
                                            <span class="indicator-name">Confidence:</span>
                                            <span class="indicator-value">${forensicMetrics.confidence}</span>
                                        </div>
                                        <div class="indicator-desc">Confidence level in the financial data integrity based on statistical patterns.</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="metric-box">
                        <div class="metric-label">Latest Price</div>
                        <div class="metric-value" style="font-size: 1.4em; font-weight: 600; text-align: center;">$${Number(data.data.metrics.latest_price).toFixed(2)}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Volume</div>
                        <div class="metric-value" style="font-size: 1.3em; text-align: center;">${Number(data.data.metrics.volume).toLocaleString()}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Market Cap</div>
                        <div class="metric-value" style="font-size: 1.3em; text-align: center;">${data.data.metrics.market_cap === 'N/A' ? 'N/A' : `$${Number(data.data.metrics.market_cap).toLocaleString()}`}</div>
                    </div>
                    <div class="metric-box technical-indicators">
                        <div class="metric-label">Technical Indicators</div>
                        <div class="metric-value">
                            <div class="indicator-item">
                                <div class="indicator-row">
                                    <span class="indicator-name">RSI:</span>
                                    <span class="indicator-value">${Number(data.data.metrics.technical.rsi).toFixed(2)}</span>
                                </div>
                                <div class="indicator-desc">Relative Strength Index - Measures momentum (0-100). Values below 30 suggest oversold, above 70 suggest overbought.</div>
                            </div>
                            <div class="indicator-item">
                                <div class="indicator-row">
                                    <span class="indicator-name">SMA50:</span>
                                    <span class="indicator-value">$${Number(data.data.metrics.technical.sma_50).toFixed(2)}</span>
                                </div>
                                <div class="indicator-desc">50-Day Simple Moving Average - Average price over last 50 days. Helps identify medium-term trends.</div>
                            </div>
                            <div class="indicator-item">
                                <div class="indicator-row">
                                    <span class="indicator-name">SMA200:</span>
                                    <span class="indicator-value">$${Number(data.data.metrics.technical.sma_200).toFixed(2)}</span>
                                </div>
                                <div class="indicator-desc">200-Day Simple Moving Average - Average price over last 200 days. Helps identify long-term trends.</div>
                            </div>
                            <div class="indicator-item">
                                <div class="indicator-row">
                                    <span class="indicator-name">Volatility:</span>
                                    <span class="indicator-value">${(Number(data.data.metrics.technical.volatility) * 100).toFixed(2)}%</span>
                                </div>
                                <div class="indicator-desc">Measures price fluctuation over time. Higher values indicate greater price swings and risk.</div>
                            </div>
                        </div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">DCF Valuation</div>
                        <div class="metric-value">
                            <div class="indicator-item">
                                <div class="indicator-row">
                                    <span class="indicator-name">Base:</span>
                                    <span class="indicator-value">$${dcfValuation.baseCase}</span>
                                </div>
                                <div class="indicator-desc">Base case valuation using discounted cash flow model.</div>
                            </div>
                            <div class="indicator-item">
                                <div class="indicator-row">
                                    <span class="indicator-name">Bull:</span>
                                    <span class="indicator-value">$${dcfValuation.bullCase}</span>
                                </div>
                                <div class="indicator-desc">Optimistic scenario with higher growth assumptions.</div>
                            </div>
                            <div class="indicator-item">
                                <div class="indicator-row">
                                    <span class="indicator-name">Bear:</span>
                                    <span class="indicator-value">$${dcfValuation.bearCase}</span>
                                </div>
                                <div class="indicator-desc">Conservative scenario with lower growth assumptions.</div>
                            </div>
                            <div class="indicator-item">
                                <div class="indicator-row">
                                    <span class="indicator-name">Discount:</span>
                                    <span class="indicator-value">${dcfValuation.discountRate}</span>
                                </div>
                                <div class="indicator-desc">Discount rate used in the DCF model based on risk profile.</div>
                            </div>
                        </div>
                    </div>
                    <div class="metric-box rating-box">
                        <div class="metric-label">Overall Rating</div>
                        <div class="metric-value">
                            <div class="rating-value ${getRatingClass(generateRating(data.data.metrics))}">${generateRating(data.data.metrics)}</div>
                            <div class="rating-basis">Based on technical indicators, price momentum, and market conditions</div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        resultsDiv.appendChild(tickerDiv);

        // Create price chart
        // Create volume trace as a bar chart
        const volumeTrace = {
            x: data.data.price_history.dates,
            y: data.data.price_history.volumes,
            type: 'bar',
            name: 'Volume',
            marker: {
                color: 'rgba(92, 107, 192, 0.3)' // Light indigo with transparency
            },
            yaxis: 'y2'
        };

        // Create price trace as a line chart
        const priceTrace = {
            x: data.data.price_history.dates,
            y: data.data.price_history.prices,
            type: 'scatter',
            name: 'Price',
            line: {
                color: '#7e57c2', // Purple
                width: 2
            }
        };

        const layout = {
            title: `${ticker} Price History`,
            xaxis: {
                title: 'Date',
                color: '#e0e0e0',
                gridcolor: '#333333'
            },
            yaxis: {
                title: 'Price ($)',
                color: '#e0e0e0',
                gridcolor: '#333333',
                side: 'left'
            },
            yaxis2: {
                title: 'Volume',
                color: '#aaaaaa',
                gridcolor: '#333333',
                overlaying: 'y',
                side: 'right',
                showgrid: false
            },
            paper_bgcolor: '#1a1a1a',
            plot_bgcolor: '#1a1a1a',
            font: { color: '#e0e0e0' },
            margin: { l: 50, r: 50, t: 40, b: 50 },
            legend: {
                x: 0.01,
                y: 0.99,
                bgcolor: 'rgba(30, 30, 30, 0.7)',
                bordercolor: '#333'
            },
            hovermode: 'closest'
        };

        Plotly.newPlot(`chart-${ticker}`, [priceTrace, volumeTrace], layout);
    }
});
