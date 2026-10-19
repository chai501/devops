import time
from urllib.error import URLError
from urllib.request import urlopen


def main():
    last_error = None

    for _ in range(30):
        try:
            with urlopen("http://127.0.0.1:5000/", timeout=2) as response:
                body = response.read().decode("utf-8")
                if response.status != 200:
                    raise SystemExit(f"Unexpected HTTP status: {response.status}")
                if body != "Hello, Jenkins Multi-Stage Pipeline!":
                    raise SystemExit(f"Unexpected response body: {body!r}")
                print(body)
                return
        except URLError as error:
            last_error = error
            time.sleep(1)

    raise SystemExit(f"Application did not become ready: {last_error}")


if __name__ == "__main__":
    main()
