# Exercise 5: Docker Security with AppArmor

**Goal:** Run a Flask container under an AppArmor profile and verify that
restricted file access and shell execution are denied.

## Files

- `app.py`, `requirements.txt`, and `Dockerfile` define the Flask image.
- `my-apparmor-profile` is the profile for the Linux host.
- `apply_apparmor.py` applies and verifies the profile through the Docker SDK.
- `test_restricted_actions.py` checks the denied actions.
- `requirements-dev.txt` includes the Docker SDK used by the scripts.

The image was built and the Flask app returned HTTP 200 without a profile.
AppArmor utilities were installed in Ubuntu WSL, but its kernel reports
`apparmor not present`; Docker does not report an active profile. Therefore,
the profile-enforcement and restricted-action tests have **not** been
verified.

To finish on an AppArmor-enabled Linux host, load the profile and run:

```bash
sudo apparmor_parser -r /etc/apparmor.d/my-apparmor-profile
docker build -t exercise5-flask-apparmor .
python3 -m pip install -r requirements-dev.txt
python3 apply_apparmor.py
python3 test_restricted_actions.py
```

**Status:** Partially complete; enforcement requires a reachable Linux host
with AppArmor enabled and sudo access.

**Original lab:** [Docker AppArmor Exercise](https://github.com/SunagP/DevOps-Lab/blob/main/Exercises/5-Docker-Security-AppArmor.md).
