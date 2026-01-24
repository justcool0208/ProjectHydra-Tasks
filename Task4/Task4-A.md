# Task 3-C: Advanced RL Environment for System Recovery

## Objective
Build a realistic RL environment that simulates Kubernetes pod failures and system recovery scenarios. This environment will serve as the foundation for training an RL agent that can learn optimal recovery actions. You will integrate Prometheus-like metrics observation and implement realistic failure injection mechanisms.

## What You'll Build
- A Kubernetes-inspired RL environment (simulated, not real infrastructure)
- A trained RL agent that learns to recover from failures
- Understanding of how to model system behavior for RL
- The foundation for Task 3-D (real Kubernetes integration)

**This is a simulation task** - you're building a realistic model of Kubernetes behavior in Python, training an RL agent on it, and preparing for real-world deployment in Task 3-D.

---

## Prerequisites
- Completion of Task 3-B (familiarity with Stable Baselines3 and custom environments)
- Understanding of Kubernetes concepts (from Task 1-B)
- Basic knowledge of system metrics (CPU, memory, latency)

---

## What You Need to Build

### 1. Kubernetes-Inspired RL Environment
Create a gymnasium environment that simulates:
- **Microservice pods** with health states (healthy, degraded, crashed)
- **System metrics** (CPU usage, memory usage, request latency, error rate)
- **Failure events** (pod crashes, CPU spikes, memory leaks, network delays)
- **Recovery actions** (restart pod, scale up/down, route traffic away)

#### What is the Pod Actually Doing?
In this simulation, each **pod represents a microservice** (like a web API or backend service) that:
- **Processes incoming requests**: The pod receives and handles HTTP requests (similar to the services in Task 1-C or Task 2-A)
- **Consumes resources**: As it processes requests, it uses CPU and memory
- **Produces metrics**: 
  - **CPU usage**: Increases with request processing load
  - **Memory usage**: Grows as requests are handled (can leak over time)
  - **Request latency**: Time taken to process requests (increases when overloaded or unhealthy)
  - **Error rate**: Percentage of requests that fail (increases when pod is degraded)
- **Can fail**: Pods can crash (become unavailable), become overloaded, or degrade in performance

**Example scenario:**
- A pod starts healthy, processing 100 requests/second
- CPU usage is at 40%, memory at 50%, latency is 50ms, error rate is 0.1%
- A workload spike occurs: request rate increases to 200 requests/second
- CPU spikes to 95%, latency increases to 500ms, error rate jumps to 5%
- The RL agent observes these metrics and decides to scale up (add more pods) to handle the load
- After scaling, metrics return to healthy ranges

**In the simulation**, you don't need to actually run HTTP servers - you just simulate:
- Request arrival rate (workload)
- How pods process requests (affecting CPU/memory)
- How failures affect processing (increasing latency/errors)

#### Implementation Approach: Simulation vs Real Service

**For Task 3-C, you have two options:**

**Option 1: Pure Simulation (Recommended for Learning)**
- **No actual HTTP service runs** - everything is simulated in Python
- You model pod behavior mathematically:
  - Request rate → affects CPU/memory usage
  - CPU overload → increases latency and error rate
  - Pod crashes → stops processing requests
- **Advantages**: Faster training, easier to debug, no infrastructure needed
- **Example**: Use formulas like `cpu_usage = min(1.0, request_rate * 0.01)`

**Option 2: Real Service Integration (More Realistic)**
- **Run actual microservices** (like the ones from Task 1-C or Task 2-A)
- Deploy them in Docker containers or Kubernetes
- Collect **real metrics** from Prometheus
- **Advantages**: More realistic, tests real system behavior
- **Disadvantages**: Slower, requires infrastructure, harder to control failure scenarios

**Recommendation**: Start with **Option 1 (Pure Simulation)** for Task 3-C to focus on RL algorithm development. You can switch to real services in Task 3-D when integrating with actual Kubernetes.

**What you're simulating:**
```python
# Example: Simulated pod behavior
class SimulatedPod:
    def __init__(self):
        self.health = "healthy"
        self.cpu = 0.0
        self.memory = 0.0
        self.latency = 50.0  # ms
        self.error_rate = 0.001
        
    def update(self, request_rate, num_pods):
        """Update metrics based on simulated request processing"""
        requests_per_pod = request_rate / num_pods
        
        # Simulate CPU usage
        self.cpu = min(1.0, requests_per_pod * 0.005)
        
        # Simulate latency (increases with load)
        if self.cpu > 0.8:
            self.latency = 50 + (self.cpu - 0.8) * 1000
        else:
            self.latency = 50
            
        # Simulate errors (increases when overloaded)
        if self.cpu > 0.9:
            self.error_rate = 0.05 + (self.cpu - 0.9) * 0.5
        else:
            self.error_rate = 0.001
```

**Note**: In Task 3-D, you WILL need real services running on Kubernetes, but for Task 3-C, simulation is sufficient and recommended.

### 2. State Space Design
Design a comprehensive state representation:
- Pod health status (one-hot encoded or numerical)
  - For multiple pods: aggregate (e.g., count of healthy/degraded/crashed pods)
  - Or: per-pod status if small number of pods (e.g., 3 pods = 3 values)
- Current metrics (CPU, memory, latency, error rate) - normalized
  - Aggregate across all pods: average CPU, average memory, average latency, average error rate
  - Normalize to [0, 1] range: CPU/100, Memory/100, latency/1000, error_rate (already 0-1)
- Time since last failure (normalized: current_step / max_episode_length)
- Current replica count (normalized: current_replicas / max_replicas, e.g., /10)
- Historical metrics (optional: last N timesteps)
  - If including: use a fixed window (e.g., last 5 timesteps) to avoid variable-length state

**Example state vector** (if using aggregated metrics):
- [healthy_pod_count, degraded_pod_count, crashed_pod_count, avg_cpu, avg_memory, avg_latency, avg_error_rate, time_since_failure, replica_count]
- Total: 9 dimensions (or more if including history)

**Recommendation**: Start simple with aggregated metrics. Add per-pod details later if needed.

### 3. Action Space Design
Define recovery actions:
- **Discrete actions**: 
  - No action
  - Restart pod
  - Scale up (add replica)
  - Scale down (remove replica)
  - Drain traffic (stop sending requests)
- Or **Continuous actions** (if using PPO with continuous action space):
  - Scale factor (0.5 to 2.0)
  - Restart probability (0 to 1)

### 4. Reward Function Design
Design a reward function that encourages:
- Fast recovery from failures
- Maintaining system health
- Minimizing unnecessary actions (cost efficiency)
- Avoiding over-scaling or under-scaling

**Example reward structure:**
- +100: System fully recovered (all pods healthy, metrics normal)
- +10: System health improved
- -10: System health degraded
- -50: System completely down (all pods crashed)
- -1: Each action taken (to encourage efficiency)
- -5: Over-scaling (too many replicas for current load)

---

## Implementation Tasks

### Task 1: Environment Core Implementation
Create `kubernetes_rl_env.py` with:
- Environment class inheriting from `gymnasium.Env`
- State space definition (use `gymnasium.spaces.Box` for continuous or `Discrete` for discrete)
- Action space definition (use `gymnasium.spaces.Discrete` for discrete actions)
- `reset()` method: Initialize system to healthy state
  - Set initial pod count (e.g., 3 pods)
  - Set all pods to "healthy"
  - Initialize metrics to normal ranges
  - Return initial observation
- `step(action)` method: 
  - Apply action (with validation: don't scale below 1 or above max)
  - Simulate system dynamics (workload changes, potential failures)
  - Update pod states and metrics
  - Calculate reward
  - Check termination: episode ends if all pods crashed OR max steps reached
  - Return (observation, reward, terminated, truncated, info)

**Episode termination conditions:**
- `terminated=True`: All pods crashed (system completely down)
- `truncated=True`: Reached maximum episode length (e.g., 200 steps)
- Otherwise: `terminated=False, truncated=False`

**Important**: This is a **simulated environment** - you're not connecting to real Kubernetes or running actual services. You're modeling pod behavior with Python code that:
- Simulates request arrival and processing
- Calculates CPU/memory usage based on workload
- Models how failures affect metrics
- Updates pod states based on actions (restart, scale, etc.)

**Example structure:**
```python
class KubernetesRLEnv(gymnasium.Env):
    def __init__(self):
        self.pods = []  # List of SimulatedPod objects
        self.request_rate = 100  # Simulated requests/second
        self.max_pods = 10  # Maximum number of pods
        self.min_pods = 1   # Minimum number of pods
        # ... define state/action spaces
        
    def step(self, action):
        # 1. Apply action (e.g., restart pod, scale up/down)
        #    - Validate: don't scale below min_pods or above max_pods
        # 2. Simulate workload (update request_rate, maybe add randomness)
        # 3. Update each pod's metrics (CPU, memory, latency) based on workload
        # 4. Check for failures (random pod crashes, CPU spikes, etc.)
        # 5. Aggregate metrics across all pods (average CPU, average memory, etc.)
        # 6. Calculate reward based on system health
        # 7. Check termination (all pods crashed? max steps reached?)
        # 8. Return observation (state vector), reward, terminated, truncated, info
```

**Pod management:**
- Start with 3 pods (all healthy)
- When scaling up: Add new pods (initialize as healthy)
- When scaling down: Remove pods (remove from list)
- When restarting: Set pod health to "restarting" for 3-5 steps, then "healthy"

**Deliverable:**
- Complete environment implementation
- Unit tests to verify environment behavior
- Visualization of state transitions

---

### Task 2: Failure Injection System
Implement a failure injection mechanism:
- **Random failures**: Pods can crash with probability p
- **Workload spikes**: Sudden increase in CPU/memory usage
- **Gradual degradation**: Slow memory leak or CPU saturation
- **Network issues**: Latency spikes or packet loss

**Failure types to simulate:**
1. Pod crash (pod becomes unavailable)
2. CPU spike (sudden 90%+ CPU usage)
3. Memory leak (gradual memory increase)
4. Network latency (response time increases)

**Deliverable:**
- Failure injection logic
- Configurable failure rates and types
- Documentation of failure scenarios

---

### Task 3: System Dynamics Simulation
Implement realistic system behavior:
- **Workload fluctuations**: Random variations in request rate
- **Recovery dynamics**: 
  - Pod restart takes 3-5 timesteps
  - Scaling takes 2-4 timesteps
  - Metrics update gradually after actions
- **Cascading failures**: One pod failure can affect others

**Implementation Example:**
```python
# Pseudocode for simulating pod behavior
class Pod:
    def __init__(self):
        self.health = "healthy"  # healthy, degraded, crashed
        self.cpu_usage = 0.0
        self.memory_usage = 0.0
        self.request_rate = 0  # requests per second
        
    def process_requests(self, incoming_request_rate):
        """Simulate how pod processes requests"""
        if self.health == "crashed":
            return  # Pod can't process requests
        
        # Distribute requests across all healthy pods
        requests_per_pod = incoming_request_rate / num_healthy_pods
        
        # CPU usage increases with request load
        self.cpu_usage = min(1.0, requests_per_pod * cpu_per_request)
        
        # Memory usage (can leak over time)
        self.memory_usage = min(1.0, base_memory + requests_per_pod * memory_per_request)
        
        # Latency increases when overloaded
        if self.cpu_usage > 0.8:
            latency = base_latency * (1 + (self.cpu_usage - 0.8) * 5)
        else:
            latency = base_latency
            
        # Error rate increases when unhealthy
        if self.health == "degraded" or self.cpu_usage > 0.9:
            error_rate = 0.05 + (self.cpu_usage - 0.9) * 0.5
        else:
            error_rate = 0.001
```

**Deliverable:**
- System dynamics implementation
- Realistic timing for actions
- Metrics update logic

---

### Task 4: Training RL Agent
Train a PPO agent on your Kubernetes environment:
- Use Stable Baselines3 PPO
- Train for 50,000+ timesteps (or until convergence)
- Implement reward shaping if needed (adjust reward function if agent doesn't learn)
- Monitor training metrics (episode reward, episode length)

**Training tips:**
- Use `tensorboard` to monitor training: `tensorboard --logdir ./logs`
- Save model checkpoints periodically
- If agent doesn't improve, try:
  - Adjusting learning rate (default 3e-4)
  - Changing network architecture
  - Adjusting reward function (make rewards less sparse)
  - Increasing training time

**Deliverable:**
- Training script: `train_kubernetes_agent.py`
- Training curves (plot reward and episode length over time)
- Trained model checkpoint (saved model file)
- Training logs (optional: TensorBoard logs)

---

### Task 5: Evaluation and Analysis
Evaluate the trained agent:
- Run 20 test episodes
- Compare with baseline policies:
  - Random agent
  - Heuristic policy (always restart on failure, scale on high CPU)
- Analyze agent behavior:
  - What actions does it take in different failure scenarios?
  - How quickly does it recover?
  - Does it learn efficient policies?

**Deliverable:**
- Evaluation script
- Comparison results (table/graph)
- Analysis of learned policy
- Visualization of agent behavior in different scenarios

---

### Task 6: Metrics Integration 
Integrate Prometheus-like metrics to track **RL training progress** (not the simulated pod metrics):
- Expose training metrics at `/metrics` endpoint using Prometheus client library
- Track:
  - Episode rewards (average, min, max)
  - Action distribution (which actions the agent chooses)
  - Recovery time (how long it takes to recover from failures)
  - System health over time (from the simulation)
- Create a simple Grafana dashboard to visualize training progress

**Note**: You're using Prometheus/Grafana to monitor the **RL training process**, not to collect metrics from real services. The simulated pod metrics (CPU, memory, etc.) are already part of your environment's state - this task is about tracking how well your RL agent is learning.

**Deliverable:**
- Metrics exporter (Python script using `prometheus_client`)
- Grafana dashboard (screenshots showing training curves)
- Prometheus configuration (to scrape your metrics endpoint)

---

## Resources

1. **RL Environment Design:**
   - [Designing RL Environments](https://towardsdatascience.com/designing-rl-environments-1b3b5c3e5a4a)
   - [Reward Shaping in RL](https://www.alexirpan.com/rl-difficulties.html)

2. **Kubernetes Concepts:**
   - [Kubernetes Pod Lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)
   - [Kubernetes Autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)

3. **Prometheus Integration:**
   - [Prometheus Python Client](https://github.com/prometheus/client_python)

---

## Deliverables

1. **Kubernetes RL Environment** (Task 1)
   - Code: `kubernetes_rl_env.py`
   - Tests and documentation

2. **Failure Injection System** (Task 2)
   - Failure injection code
   - Configuration and documentation

3. **System Dynamics** (Task 3)
   - Dynamics simulation code

4. **Trained RL Agent** (Task 4)
   - Training script: `train_kubernetes_agent.py`
   - Model checkpoint
   - Training curves

5. **Evaluation Results** (Task 5)
   - Evaluation script: `evaluate_agent.py`
   - Comparison with baselines
   - Policy analysis

6. **Metrics Integration** (Task 6, Optional)
   - Prometheus metrics exporter
   - Grafana dashboard

7. **README.md** explaining:
   - Environment design decisions
   - State/action/reward space rationale
   - Training process and results
   - Learned policy insights
   - How this prepares for real Kubernetes integration

---

## Success Criteria

- [ ] Complete Kubernetes-inspired RL environment implemented
- [ ] Failure injection system working
- [ ] Realistic system dynamics simulated
- [ ] RL agent successfully trained (improves over random baseline)
- [ ] Agent evaluated and compared with baselines
- [ ] Code is well-documented and modular
- [ ] Can explain design choices and trade-offs

---

## Design Considerations

- **State representation**: Balance between information richness and dimensionality
- **Reward shaping**: Make rewards informative but not too sparse
- **Action space**: Consider whether discrete or continuous actions are more appropriate
- **Episode length**: Long enough to see recovery, short enough for efficient training
- **Failure frequency**: Realistic but not too frequent (avoid overwhelming the agent)

