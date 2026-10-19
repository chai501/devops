# Exercise 9: Jenkins multi-stage pipeline

**Goal:** Build, test, and deploy a small Flask app through a Jenkins
Declarative Pipeline, then run it and check its HTTP response.

## Files

- `app.py` serves the exercise greeting on port 5000.
- `requirements.txt` pins Flask.
- `test_app.py` verifies the home page using Flask's test client.
- `verify_deployment.py` checks the running app's HTTP response.
- `Jenkinsfile` defines Build, Test, Deploy, and Run Application stages.
- `Dockerfile` and `docker-compose.yml` provide Jenkins with Python 3, Git,
  and a persistent Jenkins home volume.

## Start Jenkins

From this folder, start the exercise's Python-ready Jenkins controller:

```powershell
docker compose up -d --build
docker compose ps
```

The controller is bound to localhost on port 8082 by default. Open
http://127.0.0.1:8082, unlock Jenkins using the one-time password shown by:

```powershell
docker compose exec jenkins sh -c 'cat /var/jenkins_home/secrets/initialAdminPassword'
```

Complete the initial setup wizard and sign in. If host port 8082 is already
in use, set `$env:JENKINS_HTTP_PORT` to another free port before `docker
compose up`.

## Create and run the pipeline job

1. In Jenkins, choose **New Item**, enter `Python-MultiStage-Pipeline`, select
   **Pipeline**, and select **OK**.
2. Under **Pipeline**, set **Definition** to **Pipeline script from SCM**.
3. Choose **Git**, set the repository URL to
   `https://github.com/chai501/devops.git`, and set the branch specifier to
   `*/my-exercises`.
4. Set **Script Path** to
   `My-Exercises/Exercise-09-Jenkins-Multi-Stage-Pipeline/Jenkinsfile`.
5. Save and select **Build Now**. The pipeline creates a virtual environment,
   installs Flask, runs the unit test, copies the app to
   `python-app-deploy`, starts it temporarily, and verifies its HTTP response
   with `verify_deployment.py`.

Expected console output includes:

```text
Ran 1 test
OK
Hello, Jenkins Multi-Stage Pipeline!
Pipeline completed successfully!
Finished: SUCCESS
```

The application process is stopped at the end of the Run Application stage;
the copied deployment files remain in the job workspace.

Stop Jenkins with `docker compose down`. The named volume retains the Jenkins
configuration and pipeline job.

**Status:** The app and unit test are implemented and verified in a Python
container. The Jenkins controller and pipeline run still require completing
the initial setup wizard in a browser.

**Original lab:** [Jenkins Multi-Stage Pipeline Exercise](https://github.com/SunagP/DevOps-Lab/blob/main/Exercises/9-Jenkins-Multi-Stage-Pipeline.md).
