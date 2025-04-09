from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
import json
import asyncio
import logging

from src.main import analyze_stock, analyze_multiple_tickers

app = FastAPI(title="Financial Analysis Dashboard")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

logger = logging.getLogger(__name__)

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("connection open")

    try:
        while True:
            data = await websocket.receive_json()

            if data["type"] == "analyze":
                tickers = data["tickers"]
                logger.info(f"Analyzing tickers: {tickers}")

                try:
                    results = await analyze_multiple_tickers(tickers)

                    for ticker, result in results.items():
                        if 'error' in result:
                            await websocket.send_json({
                                "type": "error",
                                "message": result['error']
                            })
                            continue

                        await websocket.send_json({
                            "type": "analysis_result",
                            "ticker": ticker,
                            "data": {
                                "price_history": {
                                    "dates": result["price_history"]["dates"],
                                    "prices": result["price_history"]["prices"],
                                    "volumes": result["price_history"]["volumes"]
                                },
                                "metrics": {
                                    "latest_price": result["metrics"]["latest_price"],
                                    "volume": result["metrics"]["volume"],
                                    "market_cap": result["metrics"]["market_cap"],
                                    "technical": {
                                        "rsi": result["metrics"]["technical"]["rsi"],
                                        "sma_50": result["metrics"]["technical"]["sma_50"],
                                        "sma_200": result["metrics"]["technical"]["sma_200"],
                                        "volatility": result["metrics"]["technical"]["volatility"]
                                    }
                                }
                            }
                        })

                    await websocket.send_json({
                        "type": "analysis_complete"
                    })

                except Exception as e:
                    logger.error(f"Analysis error: {str(e)}")
                    await websocket.send_json({
                        "type": "error",
                        "message": f"Analysis failed: {str(e)}"
                    })

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
