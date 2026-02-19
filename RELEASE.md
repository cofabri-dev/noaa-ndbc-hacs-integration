# GitHub Release – Copy/Paste

Use this when creating a new release at:  
**Repo → Releases → Create a new release**

---

## Tag

```
v1.2.0
```

- **Tag version:** `v1.2.0`
- **Target:** `main` (or your default branch)
- Choose **Create new tag: v1.2.0 on publish**

---

## Release title

```
v1.2.0 – Last Updated sensor & Ocean Swim Comfort
```

---

## Describe this release (paste the block below)

```markdown
**NOAA NDBC Ocean Weather** brings buoy and coastal station data into Home Assistant: water temperature, air temperature, wind, waves, and pressure. Uses [NOAA NDBC realtime2](https://www.ndbc.noaa.gov/data/realtime2/) data—no API key required.

## What's new in v1.2.0

- **Last Updated** sensor – observation timestamp from the buoy data (UTC), i.e. when the station actually reported the observation.
- **Ocean Swim Comfort** – [OCEAN_SWIM_COMFORT.md](OCEAN_SWIM_COMFORT.md) documents a template sensor that combines air + water temp into a simple rating (Too cold / Brisk / Comfortable / Warm) and how to update the integration.

## Sensors

- **Last Updated** (new) – observation time from the buoy (UTC)  
- Water Temperature, Air Temperature, Dew Point  
- Pressure  
- Wind Direction, Wind Speed, Wind Gust  
- Wave Height, Dominant/Average Wave Period, Mean Wave Direction  

## Requirements

- Home Assistant 2023.x or newer  
- Internet access to ndbc.noaa.gov  

## Installation (HACS)

1. **HACS** → **Integrations** → **⋮** → **Custom repositories**
2. Add: `https://github.com/cofabri-dev/noaa-ndbc-hacs-integration` → **Integration**
3. Search **NOAA NDBC Ocean Weather** → **Download** → choose **v1.2.0** (or latest)
4. Restart Home Assistant, then **Settings** → **Devices & services** → **Add integration** → **NOAA NDBC Ocean Weather**
5. Enter your [NDBC Station ID](https://ndbc.noaa.gov/to_station.shtml) (e.g. `41002`, `FPSN7`)

**Manual install:** Download the `custom_components/noaa_buoy` folder from this release and place it in your Home Assistant `config/custom_components/` directory.
```

---

## Checklist

- [ ] Tag: `v1.2.0`
- [ ] Target branch: `main`
- [ ] Title and description pasted
- [ ] Click **Publish release**

In HACS, choose the **v1.2.0** release when downloading (not "Default branch") to avoid the version error.
