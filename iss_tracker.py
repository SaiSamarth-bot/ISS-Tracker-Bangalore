import ssl
import urllib.request
from skyfield.api import Topos, load

# 1. FIX for Python 3.13: Bypass SSL verification for satellite data downloads
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except AttributeError:
    pass

def track_iss():
    # 2. Setup Location: North Bangalore
    # Preserving your specific elevation for accuracy
    blr_location = Topos('13.1584 N', '77.5946 E', elevation_m=920)

    # 3. Load data using the built-in loader
    ts = load.timescale()
    t = ts.now()

    print("🛰️ Downloading latest TLE data from Celestrak...")
    url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle'
    
    try:
        satellites = load.tle_file(url)
        by_name = {sat.name: sat for sat in satellites}
        iss = by_name['ISS (ZARYA)']
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return

    # 4. Calculate Position
    difference = iss - blr_location
    topocentric = difference.at(t)
    alt, az, distance = topocentric.altaz()

    # 5. Result Display
    print("\n--- Current Orbital Status ---")
    print(f"Location: Bangalore (13.15°N, 77.59°E)")
    print(f"Time:     {t.utc_strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"Altitude: {alt.degrees:.2f}°")
    print(f"Azimuth:  {az.degrees:.2f}°")
    
    if alt.degrees > 0:
        print("\n🚀 SUCCESS: The ISS is currently in your sky!")
    else:
        print("\n🌑 STATUS: The ISS is currently below the horizon.")

if __name__ == "__main__":
    track_iss()