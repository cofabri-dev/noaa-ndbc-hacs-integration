# NOAA Buoy – Home Assistant Integration

Pull NOAA NDBC buoy data (water temperature, air temperature, wind, waves, pressure) into Home Assistant. Uses the [NDBC realtime2](https://www.ndbc.noaa.gov/data/realtime2/) text files—no API key required.

---

## Installation

### Option A: HACS (custom repository)

1. In Home Assistant, open **HACS** → **Integrations**.
2. Click the **three dots (⋮)** (top right) → **Custom repositories**.
3. Add:
   - **Repository:** `https://github.com/YOUR_USERNAME/noaa-ndbc-hacs-integration` (use your actual repo URL).
   - **Category:** **Integration**.
4. Click **ADD**, then **Close**.
5. In HACS → **Integrations**, search for **NOAA Buoy** → **Download**.
6. **Restart Home Assistant:** **Settings** → **System** → **Restart**.

### Option B: Manual

1. [Download](https://github.com/YOUR_USERNAME/noaa-ndbc-hacs-integration/archive/refs/heads/main.zip) or clone this repo.
2. Copy the **`custom_components/noaa_buoy`** folder into your Home Assistant **config** directory:
   - Target path: `config/custom_components/noaa_buoy/`
   - So you have: `config/custom_components/noaa_buoy/manifest.json`, `__init__.py`, etc.
3. **Restart Home Assistant:** **Settings** → **System** → **Restart**.

---

## Configuration

1. Go to **Settings** → **Devices & services** → **Add integration**.
2. Search for **NOAA Buoy** and select it.
3. Enter your **NDBC Station ID** (e.g. `41002` for buoys, `FPSN7` for C-MAN stations).
4. Submit. The integration will validate the station and create the device and sensors.

---

## Finding station IDs

- **[Station list](https://ndbc.noaa.gov/to_station.shtml)** – searchable list of all NDBC stations.
- **[Map](https://ndbc.noaa.gov/obs.shtml)** – interactive map; click a buoy or C-MAN station for its ID.

Use the 5-digit ID shown (e.g. `41002`). C-MAN (land) stations often use mixed case (e.g. `FPSN7`).

---

## Sensors

For each configured station you get:

| Sensor               | Description              | Unit   |
|----------------------|--------------------------|--------|
| Water Temperature    | Sea surface temperature  | °C     |
| Air Temperature      | Air temperature          | °C     |
| Dew Point            | Dew point temperature    | °C     |
| Pressure             | Sea level pressure       | hPa    |
| Wind Direction       | Wind from direction      | °      |
| Wind Speed           | Average wind speed       | m/s    |
| Wind Gust            | Peak gust speed          | m/s    |
| Wave Height          | Significant wave height  | m      |
| Dominant Wave Period | Dominant wave period     | s      |
| Average Wave Period  | Average wave period      | s      |
| Mean Wave Direction  | Wave direction           | °      |

Values show as “unavailable” when the station does not report that measurement or when data is missing (`MM` in NDBC files).

---

## Data updates

- Data is fetched about **every 30 minutes**.
- NDBC typically updates stations **hourly** (often by ~25 minutes after the hour).
- No API key or account is required; please keep the default update interval to avoid overloading NDBC.

---

## Requirements

- Home Assistant 2023.x or newer (tested on recent versions).
- Internet access to `ndbc.noaa.gov`.
