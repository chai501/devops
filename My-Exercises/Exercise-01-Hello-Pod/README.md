# Exercise 1: Kubernetes Hello Pod

**Goal:** Run an Nginx pod in Minikube, expose it with a NodePort Service, and
verify the welcome page.

## Files

- `hello-k8s.yaml` defines the Pod and Service.

## Run

```powershell
kubectl apply -f hello-k8s.yaml
kubectl get pod hello-k8s
kubectl get service hello-k8s
kubectl port-forward service/hello-k8s 18080:80
```

Open `http://127.0.0.1:18080`. The pod should be `1/1 Running`; the Nginx page
was verified with HTTP 200.

**Status:** Complete.

**Original lab:** [Kubernetes Getting Started](https://github.com/SunagP/DevOps-Lab/blob/main/Exercises/1-Kubernetes-Getting-Started.md).
