# Task 2-A: Real-Time Stock Monitoring

## Goal
Build a simple web service that shows **live stock prices**, tracks **system metrics**, and tests how the system behaves when **failures are introduced**.

---

## What You Need to Build

### 1. Stock Price Service
- Fetch stock prices continuously (every **2–5 seconds**)
- You can use:
  - Any **free public stock API**

---

### 2. Simple Web Dashboard
- Display:
- Stock name
- Current price
- Price change
- Auto-refresh data (polling every few seconds is enough)
- Show an **error message** if the backend is unavailable

---

## Observability 

### 3. Prometheus Metrics
- Add a Prometheus client to the backend
- Track the following:
- Total API requests
- API response time
- Error count
- CPU and memory usage


---

### 4. Grafana Dashboard
- Connect Grafana to Prometheus
- Create visualizations for:
- Request rate
- Response latency
- Error rate
- CPU usage
- Memory usage
- Keep the dashboard simple (**4–6 panels**)

---

## Chaos Testing

### 5. Inject Failures
Simulate failures such as:
- Stopping the backend container
- Adding CPU stress
- Introducing artificial delays in API responses

**Tools you can use:**
- `docker kill`
- Chaos Mesh / LitmusChaos 

---

### 6. Observe Behavior
- Monitor Grafana dashboards while chaos is running
- Observe and note:
- Increase in latency
- Error spikes

---
