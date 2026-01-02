# Task 2-D README

## ML Model Serving with Observability

---

## Objective

* Build a simple ML model serving service
* Expose the trained model via an API
* Track model inference behavior and performance using Prometheus
* Visualize metrics using Grafana
* Ensure the setup is Dockerized and reproducible

---

## Setting Up the Required Environment

* Python 3.10
* FastAPI
* Scikit-learn
* Prometheus client
* Docker & Docker Compose
* Grafana

All dependencies are handled through Docker.

---

## Running the Components

Command to start all services:

docker compose up --build

### Services Started

* ML inference API (FastAPI)
* Prometheus
* Grafana

### Access URLs

* FastAPI: [http://localhost:8000](http://localhost:8000)
* Prometheus: [http://localhost:9090](http://localhost:9090)
* Grafana: [http://localhost:3000](http://localhost:3000)

---

## Understanding the Workflow

* A Logistic Regression model is trained offline using the Iris dataset.
* The trained model is saved as a pickle file.
* The FastAPI application loads the model at startup.
* Users send feature values to the `/predict` endpoint.
* The model performs inference and returns predictions.
* Metrics are exposed in Prometheus format.
* Prometheus scrapes the metrics endpoint.
* Grafana visualizes inference metrics in dashboards.

---

## Steps Performed

* Trained a Logistic Regression model on the Iris dataset and saved it as `model.pkl`.
* Created a FastAPI application exposing:

  * `/predict`
  * `/health`
  * `/model-info`
  * `/metrics`
* Added input validation using Pydantic schemas.
* Integrated Prometheus client to track:

  * Total prediction requests
  * Prediction latency (histogram)
  * Prediction errors
  * Input feature values
  * Prediction output distribution
* Configured Prometheus to scrape the ML API container.
* Set up Grafana dashboards for real-time visualization.
* Added Docker volumes to persist Grafana dashboards.
* Verified metrics by generating inference traffic.

---

## Observations

* The model loads correctly at application startup.
* All API endpoints return valid responses.
* Prometheus successfully scrapes metrics.
* Grafana dashboards display real-time data.
* Dashboards persist across container restarts.
* Service communication works via Docker service names.

---

## Issues Faced & Fixes

### Prometheus Label Mismatch

* Cause: Invalid label usage in metrics.
* Fix: Corrected label names and rebuilt containers.

### Empty Grafana Query Results

* Cause: No inference traffic or narrow time range selected.
* Fix: Sent multiple prediction requests and adjusted the Grafana time range.

### Grafana Dashboards Not Persisting

* Cause: No persistent volume configured for Grafana.
* Fix: Added a Docker volume mapped to `/var/lib/grafana`.

---

## Output Screenshots

* FastAPI endpoints (`/health`, `/predict`, `/metrics`)

<img width="1920" height="1080" alt="Screenshot from 2026-01-02 19-32-38" src="https://github.com/user-attachments/assets/cf30c57c-0840-40b0-9e34-d3cd45a940d2" />

* Prometheus targets page
* Grafana dashboard panels:

  * Prediction request rate
  * Prediction latency (P95)
  * Prediction error rate
  * Input feature monitoring
  * Prediction distribution
  * Service health panel
 
<img width="1920" height="1080" alt="Screenshot from 2026-01-02 19-32-27" src="https://github.com/user-attachments/assets/798c6e47-5274-45bf-b27e-7a5388614272" />


---
