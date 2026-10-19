from pathlib import Path

import docker


IMAGE_NAME = "exercise5-flask-apparmor"
PROFILE_NAME = "my-apparmor-profile"
HOST_PORT = 5002


def main():
    client = docker.from_env()
    project_dir = Path(__file__).resolve().parent

    print("Building image from Dockerfile...")
    client.images.build(path=str(project_dir), tag=IMAGE_NAME)

    print(f"Starting container with AppArmor profile {PROFILE_NAME!r}...")
    container = client.containers.run(
        IMAGE_NAME,
        ports={"5000/tcp": HOST_PORT},
        security_opt=[f"apparmor={PROFILE_NAME}"],
        detach=True,
        name="exercise5-apparmor-test",
    )
    try:
        container.reload()
        applied_profile = container.attrs.get("AppArmorProfile", "")
        security_options = container.attrs.get("HostConfig", {}).get(
            "SecurityOpt", []
        )
        print(f"Container started: {container.short_id}")
        print(f"AppArmor profile: {applied_profile}")
        print(f"Security options: {security_options}")

        if applied_profile != PROFILE_NAME:
            raise RuntimeError(
                f"Expected AppArmor profile {PROFILE_NAME!r}; "
                f"inspect reported {applied_profile!r}. "
                f"Requested security options were {security_options!r}."
            )
    finally:
        container.stop()
        container.remove()
        print("Container stopped and removed.")


if __name__ == "__main__":
    main()
