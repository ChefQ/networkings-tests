import threading
import requests

BASE_URL = "https://socket-polling-hybrid.com"
POLL_URL = f"{BASE_URL}/poll"
METRICS_URL = f"{BASE_URL}/metrics"
INTERVAL = 2  # seconds between polls

stop_event = threading.Event()

def poll_loop():
    print(f"Polling every {INTERVAL}s. Type !END! to stop.\n")
    while not stop_event.is_set():
        try:
            poll = requests.get(POLL_URL, timeout=5).json()
            metrics = requests.get(METRICS_URL, timeout=5).json()

            msgs = poll["messages"]
            print(
                f"[{poll['time']}] "
                f"CPU: {metrics['cpu_percent']}%  "
                f"RAM: {metrics['ram_mb']} MB ({metrics['ram_percent']}%)  "
                f"| {len(msgs)} message(s)"
            )
            for m in msgs:
                print(f"  [{m['source']}] {m['content']}")
        except Exception as e:
            print(f"Poll error: {e}")
        stop_event.wait(INTERVAL)

if __name__ == "__main__":
    t = threading.Thread(target=poll_loop, daemon=True)
    t.start()

    while True:
        line = input()
        if line == "!END!":
            print("Stopping.")
            stop_event.set()
            break
