
# Task 2-A: Real-Time Stock Monitoring with Observability & Chaos Testing
---
# Objective

The goal of this task is to build a **real-time stock monitoring system** that:
- Fetches live stock prices continuously
- Exposes application and system metrics
- Visualizes metrics using Prometheus and Grafana
- Demonstrates system behavior under failure using chaos testing techniques


---

## Steps / Implementation

### 1. Stock Price Service
- Implemented a backend service using **FastAPI**
- Configured stock price fetching every **2–5 seconds** (using yahoo finance api)
- Calculated:
  - Current stock price
  - Price change compared to previous value

### 2. Web Dashboard
- Created a simple frontend/dashboard
- Displays:
  - Stock name
  - Current price
  - Price change
- Implemented auto-refresh using polling
- Displays an error message if backend service goes down

### 3. Prometheus Metrics
- Integrated `prometheus_client` in the backend
- Exposed `/metrics` endpoint
- Tracked:
  - Total API requests
  - API error count
  - API response latency
  - CPU usage
  - Memory usage

### 4. Grafana Setup
- Connected Grafana to Prometheus as a data source
- Created a dashboard with :
  - Request rate
  - Response latency
  - Error rate
  - CPU usage
  - Memory usage
- Verified real-time metric updates

### 5. Containerization
- Dockerized all services
- Used **Docker Compose** to run:
  - Backend service
  - Prometheus
  - Grafana

### 6. Chaos Testing
- Injected failures using:
  - `docker kill` to stop backend container
  - CPU stress tests
  - Artificial response delays
- Observed system behavior during failures using Grafana

---

## Observations / Outputs

- Stock prices updated in real time on the dashboard
- Prometheus successfully scraped metrics from the backend
- Grafana showed:
  - Latency spikes during delays
  - Error spikes when backend was killed
  - CPU usage increase during stress tests
- When the backend was stopped:
  - Dashboard showed error state
  - `up` metric dropped
  - Error rate increased

These observations confirm correct observability setup.

---

## Issues Faced & Fixes

### Issue 1: Grafana Dashboard Disappearing
- **Cause:** Dashboards were not persisted
- **Fix:** Enabled Grafana volume mounting and saved dashboards properly

### Issue 2: Confusion Between Prometheus Queries and Grafana Metrics
- **Cause:** Grafana initially showed only raw metrics
- **Fix:** Learned and used PromQL expressions (`rate()`, `sum()`) inside Grafana panels

---
### Screenshots

Dashboard
Frontend while working
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a6ccfa2a-db17-4738-bc58-24c692008c84" />


When backend container is killed , Frontend Response
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/52e0e530-b191-4717-aaba-1b9a64824805" />


-- First Stress
<img width="1920" height="1080" alt="Screenshot from 2025-12-29 14-38-23" src="https://github.com/user-attachments/assets/47c1e9f1-316e-4441-bc54-5a075fb9f051" />
 
-- Second Stress
<img width="1920" height="1080" alt="Screenshot from 2025-12-29 14-48-16" src="https://github.com/user-attachments/assets/0412190b-8839-4850-bae8-a712e551ec68" />

-- After delay
<img width="1920" height="1080" alt="Screenshot from 2025-12-29 13-17-35" src="https://github.com/user-attachments/assets/613d8422-c60b-4b47-abff-81c54477bdfa" />

-- After fixing all issues causing stress
<img width="1920" height="1080" alt="Screenshot from 2025-12-29 15-00-12" src="https://github.com/user-attachments/assets/55adaf5f-f8da-49e2-9a76-d37d2e961fd2" />



