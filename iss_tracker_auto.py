import urllib.request
import json
import ssl
import time
from datetime import datetime

# 1. FIX for Python 3.13 SSL
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except AttributeError:
    pass

def track_iss():
    # North Bangalore Coordinates
    MY_LAT, MY_LON = 13.1584, 77.5946

    print("  ISS TRACKER STARTING...")
    print("Updates will occur every 10 minutes. Press Ctrl+C to stop.\n")

    while True:
        try:
            # Fetch Live Data
            url = "https://api.wheretheiss.at/v1/satellites/25544"
            response = urllib.request.urlopen(url)
            data = json.loads(response.read())

            lat = float(data['latitude'])
            lon = float(data['longitude'])
            
            # Timestamp for the update
            current_time = datetime.now().strftime("%H:%M:%S")

            print(f"[{current_time}] Position: {lat:.4f}, {lon:.4f}")

            # Proximity Check
            if abs(lat - MY_LAT) < 5 and abs(lon - MY_LON) < 5:
                print(">>>  ALERT: ISS is passing near Bangalore!")
            
            print(f"Map: https://www.google.com/maps?q={lat},{lon}")
            print("-" * 30)

            # Wait for 600 seconds (10 minutes)
            print("Sleeping for 10 minutes...\n")
            time.sleep(600)

        except Exception as e:
            print(f" Error: {e}. Retrying in 60 seconds...")
            time.sleep(60)

if __name__ == "__main__":
    track_iss()
