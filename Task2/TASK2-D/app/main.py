import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from prometheus_client import generate_latest

from schemas import IrisRequest
from model import predict
from metrics import *

app = FastAPI(title="ML Model Serving")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/model-info")
def model_info():
    return {
        "model": "Logistic Regression",
        "dataset": "Iris",
        "accuracy": "~97%",
        "features": 4
    }

@app.post("/predict")
def predict_api(req: IrisRequest):
    REQUESTS.inc()
    start = time.time()

    try:
        features = [
            req.sepal_length,
            req.sepal_width,
            req.petal_length,
            req.petal_width,
        ]

        for k, v in zip(FEATURES.keys(), features):
            FEATURES[k].set(v)

        prediction = predict(features)
        PREDICTIONS.labels(pred_class=str(prediction)).inc()


        return {"prediction": int(prediction)}

    except Exception as e:
        ERRORS.inc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        LATENCY.observe(time.time() - start)

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
