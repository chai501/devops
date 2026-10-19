# Exercise 8: Create a Jenkins Hello World job

**Goal:** Configure a Jenkins Freestyle project to check out this repository,
run a shell script, and display its output in the build console.

## Files

- `hello-world.sh` prints `Hello, Jenkins!`.

## Prerequisites

Start Jenkins from Exercise 7 if it is not already running. The Exercise 7
setup uses port 8080 by default; if that port is occupied, start it on 8081:

```powershell
$env:JENKINS_HTTP_PORT = "8081"
docker compose -f ..\Exercise-07-Jenkins-CI-Automation\docker-compose.yml up -d
```

Finish Jenkins's first-run unlock and administrator setup in the browser, then
sign in at `http://127.0.0.1:8081` (or port 8080 if using the default).

## Configure the Freestyle project

1. Select **New Item**, enter `HelloWorld`, choose **Freestyle project**, and
   select **OK**.
2. Under **Source Code Management**, select **Git** and enter:
   `https://github.com/chai501/devops.git`
3. Set **Branch Specifier** to `*/my-exercises`.
4. Under **Build Steps**, select **Execute shell** and enter:

   ```sh
   sh My-Exercises/Exercise-08-Jenkins-Hello-World/hello-world.sh
   ```

5. Save the job and select **Build Now**.
6. Open the build's **Console Output**. It should include:

   ```text
   Hello, Jenkins!
   Finished: SUCCESS
   ```

The repository is public, so Jenkins can clone it without a personal access
token. Do not add credentials to this exercise or commit tokens.

**Status:** Script is implemented and its output verified in a Linux
container. The Jenkins Freestyle job still needs to be configured and run
after the controller's first-run setup is completed.

**Original lab:** [Jenkins Hello World Job](https://github.com/SunagP/DevOps-Lab/blob/main/Exercises/8-Jenkins-Hello-World-Job.md).
