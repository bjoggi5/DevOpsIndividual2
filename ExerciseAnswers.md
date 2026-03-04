# 3. Exercises

## 3.0 Contributing

Done

## 3.1 Add pre-commit Hooks

Done


## 3.2 Add a New Endpoint

Done


## 3.3 Add a CI Pipeline

Done


## 3.4 Deploy on a K8s "production" Cluster

Done



## 3.5 Questions

1. The auto-scaling did not work as expected. What could be the possible reasons?

### What happened

I load-tested the endpoint with:

```bash
hey -z 30s http://minikube.test/GitOps-Starter/api/items
```

In parallel, I watched pods and the HPA:

```bash
kubectl get pods -n default -w
kubectl get hpa -n default -w
```

At first, autoscaling didn’t happen because the HPA had no CPU metrics available. In `kubectl get hpa -w`, the CPU and memory metrics showed up as unknown (unknown/10% and unknown/80%), HPA could not observe utilization, so it had nothing to scale on.

After I enabled the metrics server, the HPA immediately started reporting real values and scaling kicked in. I saw CPU jump above my target (`cpu: 240%/10%`) and the HPA scaled up in steps until it hit my configured limit (`maxReplicas: 10`): `New size: 4`, then `New size: 8`, then `New size: 10`. Later, when the load stopped and CPU dropped (`cpu: 2%/10%`–`3%/10%`), it eventually scaled down again (`Scaled down replica set ... from 10 to 4`, reason: `All metrics below target`).

I used events to confirm the scaling decisions:

```bash
kubectl get events -n default --sort-by=.lastTimestamp \
| grep -E "SuccessfulRescale|Scaled up replica set|Scaled down replica set"
```

### Why it didn’t work (initially) and why it worked after

* **No metrics = no autoscaling.** HPA needs resource metrics (CPU/memory) to calculate utilization. Before metrics-server was enabled, the HPA showed CPU as unknown in `kubectl get hpa -w`, so it couldn’t decide to scale.

* **Once metrics-server was enabled, HPA behaved as designed.** After metrics became available, `kubectl get hpa -w` showed real utilization (e.g., `cpu: 240%/10%`), and the event log confirmed rescaling decisions like `SuccessfulRescale ... cpu resource utilization (percentage of request) above target`.

* **My target was intentionally low (10%), so scaling was aggressive.** With `targetCPUUtilizationPercentage: 10`, even a modest CPU spike can trigger scaling quickly, which explains why it ramped up to `New size: 10` (and stopped there because `maxReplicas: 10`).

* **Scale-down takes time.** Even after CPU fell back to `cpu: 2%/10%`–`3%/10%`, replicas stayed high for a while before scaling down (`reason: All metrics below target`).


2. How HPA works

* **HPA watches a metric** for a workload (usually average CPU or memory across the pods in a Deployment).
* It needs a **metrics source** (typically `metrics-server`). If metrics aren’t available, the HPA shows CPU as *unknown* and can’t scale.
* For CPU scaling, it compares **actual CPU usage** to the pod’s **CPU request** and computes “% of request”.
* If usage is **above the target** (e.g., `cpu: 240%/10%`), it **increases** the Deployment replicas (up to `maxReplicas`).
* If usage stays **below the target** (e.g., `cpu: 2–3%/10%`), it **scales down**, but usually **more slowly** to avoid bouncing up/down (“thrashing”).
