# Task 4-B: RL Agent Integration with Chaos Engineering

## Objective
Integrate your trained RL agent with a real Kubernetes cluster and chaos engineering framework. This task combines everything you've learned: RL agents, Kubernetes, Prometheus monitoring, and chaos engineering. You will build a complete self-healing system that observes real system metrics, injects controlled failures, and uses RL to learn optimal recovery strategies.

## What You'll Build
- A complete self-healing system on real Kubernetes
- Integration between your trained RL agent (from Task 3-C) and real infrastructure
- Chaos engineering experiments that test system resilience
- A production-ready autonomous recovery system

**This is the final integration task** - you're taking the simulated RL agent from Task 3-C and deploying it to work with real Kubernetes clusters, real services, and real failures. This is the core deliverable of Project HYDRA.

---

## Prerequisites
- Completion of Task 3-C (Kubernetes RL environment and trained agent)
- Kubernetes cluster setup (from Task 0 and Task 1)
- Prometheus and Grafana monitoring (from Task 2)
- Understanding of chaos engineering concepts

---

## Overview
This task involves building a **Chaos-RL Controller** that:
1. Observes real Kubernetes metrics via Prometheus
2. Injects controlled failures using chaos engineering tools
3. Uses your trained RL agent to decide recovery actions
4. Executes recovery actions via Kubernetes API
5. Learns from outcomes to improve over time

---

## What is the Service Actually Doing?

**In Task 3-D, you're working with REAL microservices** (unlike Task 3-C which was simulation). Here's what they do:

### The Microservice (The Service Being Monitored)
You'll deploy a **real web service/API** that:
- **Processes HTTP requests**: Like the services you built in Task 1-C (Hydra Base Service) or Task 2-A (Stock Price Service)
- **Exposes endpoints**: 
  - `/health` - Health check endpoint
  - `/api/...` - Your actual service endpoints (could be anything: stock prices, ML predictions, etc.)
  - `/metrics` - Prometheus metrics endpoint
- **Consumes resources**: As it handles requests, it uses:
  - **CPU**: Processing requests, running business logic
  - **Memory**: Storing request data, caching, etc.
- **Produces metrics**: Real metrics that Prometheus collects:
  - Request rate (requests per second)
  - Response latency (how long requests take)
  - Error rate (percentage of failed requests)
  - CPU and memory usage (from Kubernetes)

### Example: What Your Service Could Be
You can use any of these (or create a new one):

**Option 1: Simple Web Service** (from Task 1-C)
```python
# Flask/FastAPI service
@app.route('/health')
def health():
    return {"status": "OK"}

@app.route('/api/data')
def get_data():
    # Process request, use CPU/memory
    return {"data": "some result"}
```

**Option 2: ML Model Service** (from Task 2-D)
- Serves ML predictions
- Processes inference requests
- Uses CPU/GPU for model inference

**Option 3: Stock Price Service** (from Task 2-A)
- Fetches stock prices
- Handles API requests
- Returns real-time data

### What Happens in Practice

1. **Service is running**: Your microservice is deployed in Kubernetes, handling requests
2. **Prometheus collects metrics**: Real CPU, memory, latency, error rate from the running pods
3. **Chaos is injected**: Chaos Mesh kills a pod or stresses CPU
4. **RL Agent observes**: Sees metrics change (CPU spikes, latency increases, errors)
5. **RL Agent decides**: "Scale up" or "Restart pod" based on learned policy
6. **Action is executed**: Controller actually scales the deployment or restarts pods
7. **Service recovers**: New pods start, load distributes, metrics return to normal

### The Key Difference from Task 3-C

| Task 3-C | Task 3-D |
|---------|----------|
| **Simulated** service behavior | **Real** HTTP service running |
| Fake metrics calculated in Python | Real metrics from Prometheus |
| No actual requests | Real requests being processed |
| Just code modeling | Actual infrastructure |

**Bottom line**: In Task 3-D, you need a **real, running microservice** that processes actual HTTP requests. The RL agent monitors this real service and takes real actions to keep it healthy.

---

## Architecture Components

### 1. Chaos Controller Service
A service that orchestrates chaos experiments and RL agent decisions:
- **Metrics Collector**: Fetches metrics from Prometheus
- **State Translator**: Converts Prometheus metrics to RL state format
- **RL Agent**: Loads trained model and makes decisions
- **Action Executor**: Executes Kubernetes actions (scale, restart, etc.)
- **Chaos Injector**: Triggers chaos experiments programmatically

### 2. Chaos Engineering Integration
Integrate with a chaos engineering tool:
- **Chaos Mesh** (recommended) or **LitmusChaos**
- Inject failures: pod kills, CPU stress, memory pressure, network delays
- Monitor failure injection and system response

### 3. RL Agent Service
Deploy your trained RL agent as a service:
- Load trained model (from Task 3-C)
- Receive state observations
- Return action recommendations
- Support online learning (optional: fine-tune on real data)

---

## Implementation Tasks

### Task 1: Prometheus Metrics Integration
Build a metrics collector that:
- Connects to Prometheus API (using `requests` library or `prometheus_api_client`)
- Fetches relevant metrics using PromQL queries:
  - Pod status: Query Kubernetes pod metrics or use Kubernetes API directly
  - CPU usage: `rate(container_cpu_usage_seconds_total[5m])`
  - Memory usage: `container_memory_usage_bytes / container_spec_memory_limit_bytes`
  - Request latency: Custom metric from your service (e.g., `http_request_duration_seconds`)
  - Error rate: `rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])`
  - Replica count: Query Kubernetes API or use `kube_deployment_status_replicas`
- Converts metrics to RL state format (matching your environment from Task 3-C)
  - **Critical**: The state format MUST match exactly what your Task 3-C environment used
  - Same dimensions, same order, same normalization
  - Example: If Task 3-C used [healthy_count, degraded_count, crashed_count, avg_cpu, avg_memory, avg_latency, avg_error_rate, time_since_failure, replica_count]
    - Then Task 3-D must output the same 9 values in the same order
  - Normalize metrics the same way: CPU/100, Memory/100, latency/1000, etc.
  - Handle missing pods (if a pod is down, set its metrics to 0 or a default value)
- Handles missing metrics gracefully (use default values, log warnings)

**State format compatibility checklist:**
- [ ] State vector has same number of dimensions as Task 3-C
- [ ] Values are in same order as Task 3-C
- [ ] Normalization matches (same min/max ranges)
- [ ] Missing values handled consistently

**State format compatibility:**
- Your Task 3-C environment expects a specific state format
- Ensure the metrics collector outputs the same format (same dimensions, same normalization)
- You may need to aggregate metrics across pods (average, sum, etc.) to match simulation

**Deliverable:**
- Code: `metrics_collector.py`
- State translation logic (Prometheus metrics → RL state vector)
- Unit tests with mock Prometheus data (test with sample Prometheus responses)

---

### Task 2: Kubernetes Action Executor
Build an action executor that:
- Connects to Kubernetes API (using `kubernetes` Python client)
- Implements recovery actions:
  - **Restart pod**: Delete and let deployment recreate
  - **Scale deployment**: Update replica count
  - **Drain pod**: Add/remove labels for traffic routing
- Handles errors and retries
- Logs all actions for audit

**Deliverable:**
- Code: `k8s_action_executor.py`
- Action implementations
- Error handling and logging

---

### Task 3: Chaos Injection Controller
Integrate chaos engineering tool:
- Install and configure **Chaos Mesh** (or alternative)
- Create chaos experiments:
  - Pod kill experiment
  - CPU stress experiment
  - Memory stress experiment
  - Network delay experiment
- Build API to trigger experiments programmatically
- Monitor experiment execution

**Deliverable:**
- Chaos Mesh setup and configuration
- Code: `chaos_controller.py` (API to trigger experiments)
- Chaos experiment YAML files
- Documentation of chaos scenarios

---

### Task 4: RL Agent Service
Deploy RL agent as a service:
- Load trained model from Task 3-C (use `stable_baselines3.PPO.load()`)
- Create REST API endpoint:
  - `POST /predict`: Takes state (JSON array), returns action (JSON with action and optional confidence)
    - Input: `{"state": [0.5, 0.3, 0.1, ...]}`
    - Output: `{"action": 2, "confidence": 0.85}` (action index and optional probability)
  - `GET /health`: Health check (returns service status)
  - `POST /update`: (Optional) Online learning updates (for fine-tuning on real data)
- Handle state preprocessing (normalization, etc.)
  - Ensure input state matches training format exactly
  - Validate state dimensions match expected size

**Model loading:**
```python
from stable_baselines3 import PPO
model = PPO.load("path/to/trained_model.zip")
action, _ = model.predict(state, deterministic=True)
```

**Deliverable:**
- Code: `rl_agent_service.py` (FastAPI/Flask)
- Dockerfile for the service (include model file or mount as volume)
- API documentation (OpenAPI/Swagger if using FastAPI, or simple README)
- Test script to verify API works (send sample state, get action)

---

### Task 5: Main Orchestrator (Chaos-RL Controller)
Build the main controller that orchestrates everything:
- **Observation loop**: Periodically fetch metrics and convert to state (every 10-30 seconds)
- **Decision loop**: Query RL agent for action
- **Execution loop**: Execute actions via Kubernetes API
- **Chaos loop**: Periodically inject failures (controlled, e.g., every 5 minutes)
- **Learning loop**: (Optional) Update agent based on outcomes
  - Store (state, action, reward, next_state) tuples
  - Periodically fine-tune the model with new experiences
  - **Note**: Online learning is advanced - focus on getting the system working first, add learning later

**Controller workflow:**
```
Every iteration (e.g., every 30 seconds):
1. Fetch metrics from Prometheus → Convert to state vector
2. Query RL agent service → Get action recommendation
3. Execute action via Kubernetes API (if action is not "no action")
4. Wait and observe outcome (wait 30-60 seconds for action to take effect)
5. Calculate reward (based on metrics improvement: did CPU/latency improve?)
6. (Optional) Store experience for online learning
7. Repeat
```

**Safety features to implement:**
- Rate limiting: Don't execute actions more than once per minute
- Action validation: Check if action is safe (e.g., don't scale to 0)
- Rollback: If metrics get worse after action, log it (don't auto-rollback yet)
- Manual override: Ability to pause controller or disable actions

**Configuration (config.yaml example):**
```yaml
observation_interval: 30  # seconds
chaos_injection_interval: 300  # 5 minutes
max_replicas: 10
min_replicas: 1
rl_agent_service_url: "http://rl-agent-service:8000"
prometheus_url: "http://prometheus:9090"
```

**Deliverable:**
- Code: `chaos_rl_controller.py`
- Configuration file (YAML) for controller settings
- Logging and monitoring (log all actions, decisions, outcomes)
- Safety mechanisms (rate limiting, validation)

---

### Task 6: Deployment and Testing
Deploy the complete system:
- **Deploy test microservice**: 
  - Use a simple web service (like from Task 1-C: Flask/FastAPI with `/health` endpoint)
  - Or reuse services from Task 2-A (Stock Price) or Task 2-D (ML Model Serving)
  - This is the **service being monitored and recovered** by the RL agent
  - Deploy it as a Kubernetes Deployment with multiple replicas
  - Make sure it exposes Prometheus metrics at `/metrics`
- Deploy Prometheus and Grafana (if not already running)
- Deploy Chaos Mesh
- Deploy RL agent service (your trained model as a REST API)
- Deploy Chaos-RL Controller (the main orchestrator)
- Run end-to-end test:
  1. Start system in healthy state (microservice running, handling requests)
  2. Inject pod failure via chaos (Chaos Mesh kills a pod)
  3. Observe controller detecting failure (metrics show pod down, CPU spikes)
  4. Observe RL agent recommending action (controller queries agent, gets "scale up")
  5. Observe action execution (controller scales deployment via Kubernetes API)
  6. Verify system recovery (new pod starts, metrics return to normal)

**Deliverable:**
- Kubernetes manifests (deployments, services, configmaps)
- Docker Compose or Helm charts (optional)
- Deployment documentation
- Test results and screenshots

---

### Task 7: Monitoring and Visualization
Create comprehensive monitoring:
- **Prometheus metrics** for controller:
  - Actions taken per hour
  - Recovery time
  - System health score
  - Agent confidence/uncertainty
- **Grafana dashboard** showing:
  - System metrics (CPU, memory, latency)
  - RL agent decisions over time
  - Chaos experiments timeline
  - Recovery events and outcomes
  - Reward trends

**Deliverable:**
- Prometheus metrics exporter
- Grafana dashboard JSON
- Dashboard screenshots
- Metrics documentation

---

### Task 8: Evaluation and Analysis
Run comprehensive evaluation:
- **Baseline comparison**: Compare RL agent vs:
  - No automation (manual recovery)
  - Simple heuristic (always restart on failure)
  - Random actions
- **Metrics to track**:
  - Mean Time To Recovery (MTTR)
  - System uptime
  - Number of unnecessary actions
  - Cost efficiency (resource usage)
- **Chaos scenarios**: Test different failure types and frequencies

**Deliverable:**
- Evaluation script
- Comparison results (tables, graphs)
- Analysis report
- Recommendations for improvement

---

## Resources

1. **Chaos Engineering:**
   - [Chaos Mesh Documentation](https://chaos-mesh.org/docs/)
   - [LitmusChaos Documentation](https://litmuschaos.io/docs/)
   - [Chaos Engineering Principles](https://principlesofchaos.org/)

2. **Kubernetes Python Client:**
   - [Kubernetes Python Client](https://github.com/kubernetes-client/python)
   - [Kubernetes API Reference](https://kubernetes.io/docs/reference/kubernetes-api/)

3. **Prometheus API:**
   - [Prometheus Querying API](https://prometheus.io/docs/prometheus/latest/querying/api/)
   - [Prometheus Python Client](https://github.com/prometheus/client_python)

4. **Online Learning in RL:**
   - [Fine-tuning RL Agents](https://stable-baselines3.readthedocs.io/en/master/guide/pretraining.html)

---

## Deliverables

1. **Metrics Collector** (Task 1)
   - Code: `metrics_collector.py`
   - State translation logic

2. **Kubernetes Action Executor** (Task 2)
   - Code: `k8s_action_executor.py`
   - Action implementations

3. **Chaos Controller** (Task 3)
   - Chaos Mesh setup
   - Code: `chaos_controller.py`
   - Chaos experiment configs

4. **RL Agent Service** (Task 4)
   - Code: `rl_agent_service.py`
   - Dockerfile and deployment

5. **Main Orchestrator** (Task 5)
   - Code: `chaos_rl_controller.py`
   - Configuration files

6. **Deployment** (Task 6)
   - Kubernetes manifests
   - Deployment documentation
   - Test results

7. **Monitoring** (Task 7)
   - Prometheus metrics
   - Grafana dashboard
   - Screenshots

8. **Evaluation** (Task 8)
   - Evaluation script
   - Comparison results
   - Analysis report

9. **README.md** explaining:
   - System architecture
   - How to deploy and run
   - How chaos experiments work
   - How RL agent makes decisions
   - Evaluation results and insights
   - Future improvements

---

## Success Criteria

- [ ] Complete system deployed on Kubernetes
- [ ] Prometheus metrics successfully collected and translated
- [ ] Chaos experiments can be injected programmatically
- [ ] RL agent service deployed and responding
- [ ] Controller orchestrates observation → decision → action cycle
- [ ] System recovers from injected failures
- [ ] Monitoring dashboard shows system behavior
- [ ] Evaluation shows RL agent outperforms baselines
- [ ] All components are well-documented

---

## Safety Considerations

- **Rate limiting**: Don't execute actions too frequently (max 1 action per minute)
- **Safety checks**: Verify actions before execution (e.g., don't scale to 0, don't scale above max)
- **Rollback mechanism**: Ability to disable RL controller quickly (kill pod or set flag)
- **Human oversight**: Log all actions for review (who/what/when/why)
- **Gradual rollout**: 
  1. Start with **read-only mode**: Controller observes but doesn't execute actions
  2. Then **manual approval mode**: Controller suggests actions, human approves
  3. Finally **autonomous mode**: Controller executes actions automatically
- **Testing**: Test in a separate namespace or cluster first, not production
- **Monitoring**: Set up alerts if controller takes unexpected actions

---

## Optional Enhancements

- **Explainability**: Add SHAP/LIME to explain agent decisions

---


