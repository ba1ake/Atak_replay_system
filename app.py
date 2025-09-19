import os
import time
import requests
import xml.etree.ElementTree as ET
from datetime import datetime




####!SECTION Varibles and files

EXPORT_LINKS = [ # need to set this to the KML from atak, ensure you add IP and port 8443 not 8446
]





event = str( datetime.utcnow().strftime("%Y-%m-%d %H"))
SAVE_DIR = "atak_logs"
SCRAPE_INTERVAL = 60  # this be default is 60 seconds
CERT_FILE = "admin.pem"  





def fetch_kml(url: str) -> str:
    """Fetch raw KML XML from a URL using .pem client cert."""
    try:
        response = requests.get(
            url,
            verify=False,         
            cert=CERT_FILE,       
            timeout=60,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"[ERROR] Could not fetch {url}: {e}")
        return None


def parse_kml(kml_data: str) -> list:
    """Parse KML and extract Placemark details."""
    try:
        root = ET.fromstring(kml_data)
        ns = {"kml": "http://www.opengis.net/kml/2.2"}

        data_points = []
        for placemark in root.findall(".//kml:Placemark", ns):
            name = placemark.find("kml:name", ns)
            coords = placemark.find(".//kml:coordinates", ns)

            user = name.text if name is not None else "Unknown"
            location = coords.text.strip() if coords is not None else "N/A"

            data_points.append({
                "user": user,
                "location": location
            })

        return sorted(data_points, key=lambda x: x["user"])

    except Exception as e:
        print(f"[ERROR] Could not parse KML: {e}")
        return []


def save_snapshot(data: list):
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    filename = os.path.join(SAVE_DIR, (event+".log"))

    with open(filename, "a") as f:  # append mode
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"\n--- Snapshot at {timestamp} UTC ---\n")
        for entry in data:
            f.write(f"[{timestamp}] {entry['user']}: {entry['location']}\n")

    print(f"[INFO] Appended snapshot -> {filename}")



if __name__ == "__main__":

    if EXPORT_LINKS == False: # verifys that KML links exsit
        print("warnnig KML source not set, please add this")
        exit



    print("Scraping data")
    while True:
        for link in EXPORT_LINKS:
            kml = fetch_kml(link)
            if not kml:
                continue

            parsed = parse_kml(kml)
            if parsed:
                if "a-f" in link: team = "Friendlies"
                else: team = "Other"

                save_snapshot(parsed)

        time.sleep(SCRAPE_INTERVAL)
