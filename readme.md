# 🛰️ ATAK KML Scraper

This Python script allows you to fetch real-time KML data from an ATAK server, parse it, and save snapshots of user positions over time. It supports **client certificate authentication** and organizes the KML data in a human-readable log format.

---

## 📄 Table of Contents

<ul>
  <li><a href="#prerequisites">Prerequisites</a></li>
  <li><a href="#converting-p12-to-pem">Converting the .p12 Key to admin.pem</a></li>
  <li><a href="#fetching-the-kml-file">Fetching the KML File from the ATAK Server</a></li>
  <li><a href="#configuring-exportlinks">Configuring the KML URL in the Script</a></li>
  <li><a href="#data-layout">Understanding the Data Layout</a></li>
  <li><a href="#running-the-script">Running the Script</a></li>
  <li><a href="#tips">Tips</a></li>
</ul>

---

## <a name="prerequisites"></a>⚙️ Prerequisites

* Python 3.13+
* `requests` library
* `requests_pkcs12` library (if using `.p12` directly)
* Access to the ATAK server and the client certificate

Install Python libraries via:

```bash
pip install requests requests_pkcs12
```

---

## <a name="converting-p12-to-pem"></a>🔑 Converting the `.p12` Key to `admin.pem`

If you have a `.p12` client certificate, you can export it as a combined PEM file:

1. Open **MMC Certificate Manager** on Windows.
2. Import your `.p12` file into **Personal certificates**.
3. Right-click the certificate → **All Tasks → Export**.
4. Choose **Yes, export the private key**.
5. Select the **Base-64 encoded X.509 (.CER)** format for the certificate.
6. Save the certificate and private key into a single `admin.pem` file like this:

```text
-----BEGIN CERTIFICATE-----
(your certificate)
-----END CERTIFICATE-----
-----BEGIN PRIVATE KEY-----
(your private key)
-----END PRIVATE KEY-----
```

> Make sure the private key matches the certificate; Python `requests` will need both.

---

## <a name="fetching-the-kml-file"></a>🌐 Fetching the KML File from the ATAK Server

1. Log in to your ATAK web portal with your admin certificate.
2. Navigate to the **Marti / Latest KML** endpoint.
3. Copy the full HTTPS URL for the feed you want to monitor, e.g.:

```text
https://serverip:8446/Marti/LatestKML?cotType=a-f&secago=60
```

---

## <a name="configuring-exportlinks"></a>📝 Configuring the KML URL in the Script

Open `app.py` and find the `EXPORT_LINKS` array (line 12). Add your KML URLs like this:

```python
EXPORT_LINKS = [
    "https://serverip:8446/Marti/LatestKML?cotType=a-f&secago=60",
    # "add more URLs here if needed"
]
```

Each URL in the array will be fetched in sequence at the interval specified in `SCRAPE_INTERVAL`.

---

## <a name="data-layout"></a>📊 Understanding the Data Layout

Once the script fetches a KML snapshot, it parses and saves it into `atak_logs` in a **log format**:

```text
--- Snapshot at 2025-09-19 14:30:05 UTC ---
[2025-09-19 14:30:05] User1: -122.401,37.789,0
[2025-09-19 14:30:05] User2: -122.402,37.790,0
[2025-09-19 14:30:05] Friendlies: -122.400,37.788,0
```

**Explanation of fields:**

<ul>
  <li><b>Timestamp:</b> UTC time of the snapshot</li>
  <li><b>User:</b> Name of the ATAK client</li>
  <li><b>Location:</b> Coordinates in <i>longitude,latitude,altitude</i> format</li>
</ul>

Snapshots are **appended** to the log file named by the hour:

```text
atak_logs/2025-09-19 14.log
```

This allows easy tracking of movement over time.

---

## <a name="running-the-script"></a>🚀 Running the Script

```bash
python app.py
```

* The script runs continuously, fetching KML every `SCRAPE_INTERVAL` seconds.
* Logs are appended in `atak_logs`.
* Insecure HTTPS warnings are suppressed for local testing.

---

## <a name="tips"></a>💡 Tips

* Make sure the certificate has **access permissions** for the feed.
* Ensure the KML URL is **exact**; even a minor change can result in `403 Forbidden`.
* You can extend `EXPORT_LINKS` to fetch multiple feeds simultaneously.
