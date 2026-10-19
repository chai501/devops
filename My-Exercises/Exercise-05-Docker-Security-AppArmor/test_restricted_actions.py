import docker


IMAGE_NAME = "exercise5-flask-apparmor"
PROFILE_NAME = "my-apparmor-profile"


def main():
    client = docker.from_env()
    container = client.containers.run(
        IMAGE_NAME,
        security_opt=[f"apparmor={PROFILE_NAME}"],
        detach=True,
        name="exercise5-apparmor-restrictions",
    )
    try:
        container.reload()
        applied_profile = container.attrs.get("AppArmorProfile", "")
        if applied_profile != PROFILE_NAME:
            raise RuntimeError(
                f"Expected AppArmor profile {PROFILE_NAME!r}; "
                f"inspect reported {applied_profile!r}."
            )

        file_result = container.exec_run(
            ["python", "-c", "open('/etc/passwd').read()"]
        )
        shell_result = container.exec_run(["/bin/bash", "-c", "true"])

        print(
            "Attempt to read /etc/passwd: "
            f"Exit Code {file_result.exit_code}, "
            f"Output: {file_result.output.decode(errors='replace').strip()}"
        )
        print(
            "Attempt to execute /bin/bash: "
            f"Exit Code {shell_result.exit_code}, "
            f"Output: {shell_result.output.decode(errors='replace').strip()}"
        )

        if file_result.exit_code == 0 or shell_result.exit_code == 0:
            raise RuntimeError("An AppArmor-restricted action unexpectedly succeeded.")
    finally:
        container.stop()
        container.remove()
        print("Container stopped and removed.")


if __name__ == "__main__":
    main()
