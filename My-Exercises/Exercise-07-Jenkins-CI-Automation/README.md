# Exercise 7: Jenkins CI automation and installation

**Goal:** Run Jenkins in Docker, complete the first-run setup, and verify that
the controller is available in a browser.

## Files

- `docker-compose.yml` starts the official Jenkins LTS image and persists
  Jenkins configuration and build data in a named volume.

The HTTP port is bound to localhost only. The inbound agent port is not
published because this single-controller exercise does not configure agents.

## Run on Windows

From this folder, start Jenkins:

```powershell
docker compose up -d
docker compose ps
```

Open http://127.0.0.1:8080 and retrieve the one-time unlock password in a
second terminal:

```powershell
docker compose exec jenkins sh -c 'cat /var/jenkins_home/secrets/initialAdminPassword'
```

Enter the password in the setup wizard, install the suggested plugins, and
create an administrator account. Keep the generated password private; do not
save it in this repository.

If port 8080 is already in use, choose another host port before starting:

```powershell
$env:JENKINS_HTTP_PORT = "8081"
docker compose up -d
```

Then open http://127.0.0.1:8081. The setting only changes the host-side port;
Jenkins continues listening on port 8080 inside the container.

Stop Jenkins with `docker compose down`. The named volume retains the setup
and data, so a later `docker compose up -d` resumes the same instance.

**Status:** Jenkins is running and the login page was verified. Complete the
one-time browser wizard to finish administrator setup.

**Original lab:** [Jenkins CI Automation Exercise](https://github.com/SunagP/DevOps-Lab/blob/main/Exercises/7-Jenkins-CI-Automation.md).
