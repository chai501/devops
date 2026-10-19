import os
import random
import time

from prometheus_client import Gauge, Summary, start_http_server

total_deliveries = Gauge("total_deliveries", "Total number of deliveries")
pending_deliveries = Gauge(
    "pending_deliveries", "Number of pending deliveries"
)
on_the_way_deliveries = Gauge(
    "on_the_way_deliveries", "Number of deliveries on the way"
)
average_delivery_time = Summary(
    "average_delivery_time", "Average delivery time in seconds"
)


def simulate_delivery():
    pending = random.randint(
        int(os.getenv("PENDING_DELIVERIES_MIN", "10")),
        int(os.getenv("PENDING_DELIVERIES_MAX", "20")),
    )
    on_the_way = random.randint(5, 20)
    delivered = random.randint(30, 70)
    avg_time = random.uniform(
        float(os.getenv("DELIVERY_TIME_MIN", "15")),
        float(os.getenv("DELIVERY_TIME_MAX", "45")),
    )

    total = pending + on_the_way + delivered
    total_deliveries.set(total)
    pending_deliveries.set(pending)
    on_the_way_deliveries.set(on_the_way)
    average_delivery_time.observe(avg_time)

    print(
        f"total={total} pending={pending} on_the_way={on_the_way} "
        f"delivery_time_seconds={avg_time:.2f}",
        flush=True,
    )


if __name__ == "__main__":
    start_http_server(8000, addr="0.0.0.0")
    print("Delivery metrics available on :8000/metrics", flush=True)
    while True:
        simulate_delivery()
        time.sleep(1)
