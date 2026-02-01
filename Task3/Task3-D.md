# Task 3-D: Run ChaosMesh Experiments and Collect Metrics

## Experiment 1: Kill Backend API Pods

Chaos Type: `PodChaos` (pod-kill)

Real-World Scenario:

- Pod crash
- Bad deployment
- OOM kill

Fault Injection:

- Randomly kill 1 backend pod (or all, if single replica)

What You Validate:

- Kubernetes restarts pods automatically
- Service endpoint remains reachable

Metrics to Watch (Grafana):

- Error rate spike
- Request drop
- Pod restart count

## Experiment 2: Backend Completely Down

Chaos Type: `PodChaos` (all pods)

Real-World Scenario:
- Full service outage
- Bad config pushed to prod

Fault Injection:

- Kill all backend pods

What You Validate:

- Frontend shows clear “Backend unavailable” message
- No frontend crash
- Alerts trigger in Prometheus (optional)

Metrics to Watch:

- 100% error rate
- Zero successful requests
- Recovery time after pods return

## Experiment 3: CPU Stress on Backend API

Chaos Type: `StressChaos` (cpu)

Real-World Scenario:

- Traffic spike
- Inefficient API logic
- External API slowdown causing busy loops

Fault Injection:

- Apply 80–90% CPU stress on backend pods

What You Validate:
- Response latency increases (but no crash)
- If HPA enabled:
  - New backend pods are created
- Frontend still updates (slower is OK)

Metrics to Watch:
- CPU usage
- Response latency
- Request success rate

## Experiment 4: Artificial API Delay

Chaos Type: `NetworkChaos` (delay)
(or app-level sleep if simpler)

Real-World Scenario:

- Stock API responding slowly
- Network congestion

Fault Injection:

- Add 500–1500 ms delay to backend responses

What You Validate:

- Prometheus latency metrics increase
- Frontend still renders data (with delay)
- No timeout crashes

Metrics to Watch:

- p95 / p99 response latency
- Request rate stability

## Experiment 5: Memory Pressure on Backend

Chaos Type: `StressChaos` (memory)

Real-World Scenario:

- Memory leak
- Large JSON responses
- Cache misconfiguration

Fault Injection:

- Gradually consume pod memory

What You Validate:

- Pod is OOM-killed
- Kubernetes restarts pod
- Service recovers automatically

Metrics to Watch:

- Memory usage
- Pod restarts
- Error spikes during restart

## Experiment 6: Sudden Client Surge

Chaos Type: `StressChaos` (cpu) + load test

Real-World Scenario:

- Market open
- Many users refreshing dashboard

Fault Injection:

- Generate high request load
- Optional: kill one backend pod mid-load

What You Validate:

- Backend remains responsive
- HPA scales pods (if enabled)
- No cascading failures

Metrics to Watch:
- Request rate
- Latency
- Pod replica count

