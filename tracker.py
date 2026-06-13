import requests
from datetime import datetime
from zoneinfo import ZoneInfo

LOCATIONS = [
    {
        "id": 579641,
        "name": "dansweiler_weg.csv"
    },
    {
        "id": 410223,
        "name": "vitalisstrasse.csv"
    }
]

def fetch(location_id):
    url = f"https://www.electromaps.com/mapi/v2/locations/{location_id}"

    r = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    r.raise_for_status()

    return r.json()

def parse(data):
    connectors = data["connectors"]

    total = len(connectors)
    occupied = sum(
        1 for c in connectors
        if c["status"] == "OCCUPIED"
    )

    return total, occupied

def save(filename, total, occupied):
    now = datetime.now(
        ZoneInfo("Europe/Berlin")
    ).strftime("%Y-%m-%d %H:%M:%S")

    with open(filename, "a") as f:
        f.write(f"{now},{total},{occupied}\n")

    print(f"{filename}: {now} → {occupied}/{total}")

def main():
    for location in LOCATIONS:
        try:
            data = fetch(location["id"])

            total, occupied = parse(data)

            save(
                location["name"],
                total,
                occupied
            )

        except Exception as e:
            print(
                f"Fehler bei {location['id']}: {e}"
            )

if __name__ == "__main__":
    main()
