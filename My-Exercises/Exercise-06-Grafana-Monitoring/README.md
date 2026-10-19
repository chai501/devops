# Exercise 6: Grafana Delivery Monitoring

**Goal:** Export simulated delivery metrics, scrape them with Prometheus,
visualize them in Grafana, alert on high values, and build the exporter in
Jenkins.

## Files

- `delivery_metrics.py`, `requirements.txt`, and `Dockerfile` implement the
  Prometheus exporter.
- `prometheus.yml` and `alert_rules.yml` configure scraping and alerts.
- `grafana/provisioning/` provisions a Prometheus datasource and four-panel
  dashboard.
- `docker-compose.yml` runs the monitoring stack.
- `Jenkinsfile` validates the source and Compose configuration, then builds
  the exporter image.
- `jenkins/` defines the local Jenkins container and provisions its pipeline
  job.

## Run

```powershell
docker compose up -d --build
```

- Metrics: http://localhost:8000/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

Prometheus targets were healthy, the Grafana datasource and dashboard loaded,
and both alert rules were observed firing.

Start Jenkins separately with a locally generated password:

```powershell
$env:JENKINS_ADMIN_PASSWORD = [guid]::NewGuid().ToString("N")
docker volume create exercise-06-grafana-monitoring_exercise6-jenkins-data
docker compose -f jenkins/docker-compose.yml up -d --build
```

Jenkins is bound to localhost on port 8080. The `Exercise6-Delivery-Pipeline`
job's build #4 completed successfully and built the delivery-metrics image.
The Docker socket mount grants Jenkins control of the local Docker engine; use
this setup only on a trusted development machine.

Stop the services with `docker compose down` and
`docker compose -f jenkins/docker-compose.yml down`.

**Status:** Complete.

**Original lab:** [Grafana Delivery Monitoring Exercise](https://github.com/SunagP/DevOps-Lab/blob/main/Exercises/6-Grafana-Realtime-Monitoring-of-Quick-Commerce-App.md).
