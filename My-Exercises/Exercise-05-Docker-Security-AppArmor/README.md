# Exercise 5: Docker Security with AppArmor

**Goal:** Run a Flask container under an AppArmor profile and verify that
restricted file access and shell execution are denied.

## Files

- `app.py`, `requirements.txt`, and `Dockerfile` define the Flask image.
- `my-apparmor-profile` is the profile loaded by the Linux host.
- `apply_apparmor.py` applies and verifies the profile through the Docker SDK.
- `test_restricted_actions.py` verifies both denied actions.
- `requirements-dev.txt` includes the Docker SDK used by the scripts.
- `.gitattributes` keeps the AppArmor profile LF-terminated when checked out
  on Windows; the Linux parser rejects the CRLF version.

## Verified results

The exercise was completed in a local Ubuntu 24.04.5 VirtualBox VM with
AppArmor enabled. The AppArmor kernel module was loaded, and the custom profile
was in enforce mode. `apply_apparmor.py` confirmed that Docker attached
`my-apparmor-profile` to the container.

`test_restricted_actions.py` passed:

- Reading `/etc/passwd` failed with `PermissionError`.
- A Python process inside the container could not execute `/bin/bash`; it
  failed with `PermissionError`.

The shell test performs the execution attempt from a Python process already
confined by AppArmor. Launching Bash directly with Docker `exec` starts a new
process and does not test whether the confined application can execute it.

The local VM is named `Exercise5-Ubuntu`. Its host SSH forward is port 2222:

```bash
ssh -i <path-to-private-key> -p 2222 ubuntu@127.0.0.1
```

## Reproduce on an AppArmor-enabled Linux host

From this exercise directory:

```bash
sudo install -o root -g root -m 0644 my-apparmor-profile /etc/apparmor.d/my-apparmor-profile
sudo apparmor_parser -r /etc/apparmor.d/my-apparmor-profile
sudo aa-status
docker build -t exercise5-flask-apparmor .
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python apply_apparmor.py
python test_restricted_actions.py
```

**Status:** Complete and verified on an AppArmor-enabled Ubuntu VM. Ubuntu
under WSL on this host does not enable AppArmor in its kernel.

**Original lab:** [Docker AppArmor Exercise](https://github.com/SunagP/DevOps-Lab/blob/main/Exercises/5-Docker-Security-AppArmor.md).
