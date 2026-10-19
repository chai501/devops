# Exercise 3: Scale Flask with ReplicaSets

**Goal:** Deploy the Flash Sale Flask app, scale its ReplicaSet, and observe
Kubernetes replace a deleted pod.

## Files

- `app.py` implements the home, checkout, and health endpoints.
- `requirements.txt` and `Dockerfile` build the Gunicorn-served app image.
- `flashsale-replicaset.yaml` defines the ReplicaSet and ClusterIP Service.

## Run

```powershell
docker build -t flashsale:1.0 .
minikube image load flashsale:1.0
kubectl apply -f flashsale-replicaset.yaml
kubectl scale rs/flashsale-rs --replicas=5
kubectl get pods -l app=flashsale -o wide
```

Deleting one pod caused the ReplicaSet to create a replacement. All five pods
were `Running` and `Ready`. The `/`, `/buy?user=123`, and `/health` endpoints
were verified through the Service.

**Status:** Complete.

**Original lab:** [ReplicaSet Scaling Exercise](https://github.com/SunagP/DevOps-Lab/blob/main/Exercises/3-Minikube-Scaling-Flask-App-with-Replicasets.md).
