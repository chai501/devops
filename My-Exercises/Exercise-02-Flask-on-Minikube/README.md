# Exercise 2: Flask on Minikube

**Goal:** Containerize a small Flask app, deploy it to Minikube, and expose it
through a Kubernetes Service.

## Files

- `app.py` serves the exercise greeting on port 15000.
- `requirements.txt` and `Dockerfile` define the app image.
- `flask-deployment.yaml` defines the Deployment and NodePort Service.

## Run on Windows

From this folder, build the image with Docker Desktop, load it into Minikube,
and apply the resources:

```powershell
docker build -t flask-app:latest .
minikube image load flask-app:latest
kubectl apply -f flask-deployment.yaml
kubectl rollout status deployment/flask-app
kubectl port-forward service/flask-app-service 15000:15000
```

Open `http://127.0.0.1:15000`. The deployment reached `1/1` ready, and the app
returned the expected greeting with HTTP 200.

**Status:** Complete.

**Original lab:** [Minikube Flask Exercise](https://github.com/SunagP/DevOps-Lab/blob/main/Exercises/2-Minikube-Kubectl-Flask.md).
