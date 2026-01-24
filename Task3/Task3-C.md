# Task 3-C: Kubernetes-Based Stock Monitoring with Chaos Engineering

## Goal

Migrate the existing **Docker Compose–based stock monitoring system** to a **Kubernetes cluster**, integrate **chaos engineering tools**, and observe system behavior, metrics, and self-recovery under controlled failures.

---

## What You Need to Build

---

## 1. Kubernetes Migration

Convert the existing Docker Compose setup into Kubernetes resources.

### Requirements

Deploy the following components to Kubernetes:

- **Stock Price Backend Service**
- **Web Dashboard (Frontend)**
- **Prometheus**
- **Grafana**

Use the following Kubernetes resources:

- `Deployment` and `Service`
- `ConfigMap` for configuration
- `Namespace` for isolation (e.g., `stock-monitoring`)

Ensure:

- All services are reachable internally via Kubernetes DNS
- The frontend is exposed using one of:
  - `NodePort`
  - `Ingress`
  - `LoadBalancer`

**Outcome**  
The application should function identically to the Docker Compose version.

---

## 2. Kubernetes-Native Observability

Integrate observability components with Kubernetes.

### Prometheus

Deploy Prometheus using one of the following:

- Helm
- Kubernetes manifests

Configure Prometheus to:

- Scrape backend application metrics
- Collect Kubernetes node and pod metrics using:
  - `kube-state-metrics`
  - `node-exporter`

### Metrics to Track

- Total API requests
- Request latency
- Error count
- Pod CPU usage
- Pod memory usage
- Pod restart count

**Outcome**  
Metrics are visible in Prometheus and queryable using PromQL.

---

## 3. Grafana Dashboards

Connect Grafana to Prometheus.

### Dashboard Requirements (4–6 panels)

- API request rate
- API response latency (p95)
- Error rate
- Pod CPU usage
- Pod memory usage
- Pod restart count

**Outcome**  
A Kubernetes-aware Grafana dashboard showing both application and infrastructure health.

---

## Chaos Engineering

---

## 4. Chaos Tool Integration

Install one chaos engineering tool:

- **Chaos Mesh** 
- **LitmusChaos**

Deploy the chaos tool in a **dedicated namespace**.

**Outcome**  
Chaos engine is running and ready to inject faults.

---

## 5. Chaos Experiments

Create and run chaos experiments targeting the **backend service**.

### Required Experiments (Minimum 3)

#### 1. Pod Failure
- Randomly kill backend pods
- Observe Kubernetes self-healing (automatic pod recreation)

#### 2. CPU Stress
- Inject high CPU load into backend pods
- Observe increased latency and resource saturation

#### 3. Network or Delay Injection
- Add artificial latency or packet loss
- Observe impact on request latency and error rate

**Outcome**  
Chaos experiments are successfully executed and logged.

---

## 6. Observe & Analyze System Behavior

While chaos experiments are running:

- Monitor Grafana dashboards
- Observe:
  - Latency spikes
  - Error rate increases
  - CPU/memory saturation
  - Pod restarts and rescheduling

After chaos stops, verify:

- The system recovers automatically
- Metrics stabilize
- Service remains available

**Outcome**  
Demonstrated **self-recovery** through Kubernetes mechanisms.

---

## Deliverables

- Kubernetes manifests or Helm values
- Chaos experiment YAML files
- Grafana dashboard JSON
- Short report including:
  - Screenshots of dashboards during chaos
  - Observed failure patterns
  - Explanation of recovery behavior
