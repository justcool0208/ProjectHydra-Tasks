from fastapi import FastAPI, HTTPException, Response
import yfinance as yf
import time
import psutil

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REQUEST_COUNT = Counter("api_requests_total", "Total API requests")
ERROR_COUNT = Counter("api_errors_total", "Total API errors")

LATENCY = Histogram("api_response_latency_seconds", "API latency")

CPU_USAGE = Gauge("cpu_usage_percent", "CPU usage")
MEMORY_USAGE = Gauge("memory_usage_percent", "Memory usage")

# Chaos Flag
CHAOS_DELAY = False

@app.get("/stock/{symbol}")
@LATENCY.time()
def get_stock(symbol: str):
    REQUEST_COUNT.inc()
    start = time.time()
    try:
        if CHAOS_DELAY:
            time.sleep(random.uniform(1, 5))  

        stock = yf.Ticker(symbol)

        price = stock.info["regularMarketPrice"]
        prev = stock.info["previousClose"]

        LATENCY.observe(time.time() - start)
    

        change = price - prev

        return {
            "symbol": symbol.upper(),
            "price": round(price, 2),
            "change": round(change, 2)
        }

    except Exception:
        ERROR_COUNT.inc()
        raise HTTPException(status_code=500, detail="Stock fetch failed")

@app.get("/metrics")
def metrics():
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.virtual_memory().percent)
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

@app.post("/chaos/delay")
def chaos_delay(enable: bool):
    global CHAOS_DELAY
    CHAOS_DELAY = enable
    return {"delay_enabled": CHAOS_DELAY}
