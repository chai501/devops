# Exercise 4: Docker Networking

**Goal:** Connect the Flask API, MySQL, and Redis containers on a Docker bridge
network.

## Files

- `app.py`, `requirements.txt`, and `Dockerfile` define the Flask API.
- `docker-compose.yml` creates an isolated bridge network and starts all three
  services.

## Run

Set a temporary lab password and start the stack from this folder:

```powershell
$env:MYSQL_ROOT_PASSWORD = [guid]::NewGuid().ToString("N")
docker compose up -d --build
docker compose ps
Invoke-RestMethod http://127.0.0.1:5001/about
```

From the Flask container, the `mysql` and `redis` service names resolve and
their TCP ports 3306 and 6379 are reachable. Redis returned `PONG`, MySQL
reported that it was alive, and `/about` returned the expected API details.

Stop the lab with `docker compose down`.

**Status:** Complete.

**Original lab:** [Docker Networking Exercise](https://github.com/SunagP/DevOps-Lab/blob/main/Exercises/4-Docker-Networking.md).
