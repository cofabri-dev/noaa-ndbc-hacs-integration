# Ocean Swim Comfort template sensor

Add a template sensor that combines **Air Temperature** and **Water Temperature** from the NOAA NDBC Ocean Weather integration into a simple "Ocean Swim Comfort" rating (Too cold / Brisk / Comfortable / Warm).

## 1. Find your entity IDs

The integration creates one device per station with sensors like **Air Temperature** and **Water Temperature**. Entity IDs look like:

- `sensor.noaa_ndbc_ocean_weather_41122_air_temperature`
- `sensor.noaa_ndbc_ocean_weather_41122_water_temperature`

Replace **41122** with your NDBC station ID (e.g. 41002, FPSN7).

To get the exact IDs in Home Assistant:

1. **Developer Tools** → **States**.
2. Filter by `noaa` or search for your station ID.
3. Copy the `entity_id` for **Air Temperature** and **Water Temperature**.

## 2. Add the template

In your **`configuration.yaml`**, under `template:` (create the key if you don’t have it), add:

```yaml
template:
  - sensor:
      - name: "Ocean Swim Comfort"
        unique_id: ocean_swim_comfort
        state: >
          {% set air_c = states('sensor.noaa_ndbc_ocean_weather_41122_air_temperature') | float(none) %}
          {% set water_c = states('sensor.noaa_ndbc_ocean_weather_41122_water_temperature') | float(none) %}
          {% if air_c is none or water_c is none %}
            Unknown
          {% else %}
            {% set water_f = (water_c * 9 / 5) + 32 %}
            {% if water_f < 70 %}
              Too cold
            {% elif water_f < 73 %}
              Brisk
            {% elif water_f < 79 %}
              Comfortable
            {% else %}
              Warm
            {% endif %}
          {% endif %}
        attributes:
          air_f: "{{ ((states('sensor.noaa_ndbc_ocean_weather_41122_air_temperature') | float(0)) * 9 / 5 + 32) | round(1) }}"
          water_f: "{{ ((states('sensor.noaa_ndbc_ocean_weather_41122_water_temperature') | float(0)) * 9 / 5 + 32) | round(1) }}"
```

Replace **41122** in all four entity IDs with your station ID (or your actual entity IDs from Developer Tools).

## 3. Reload the Template integration

After saving `configuration.yaml`:

1. **Settings** → **Devices & services** → **Template** (under Helpers).
2. Click the **three dots (⋮)** → **Reload**.

Or from **Developer Tools** → **YAML** → **Template entities**: **Reload**.

You should see **Ocean Swim Comfort** under **Template** (or under your NOAA device if you later move it there). The integration reports temperatures in °C; the template converts to °F for the comfort bands and for the `air_f` / `water_f` attributes.

---

## Updating the NOAA NDBC Ocean Weather integration

### If you installed via HACS

1. Open **HACS** → **Integrations**.
2. Find **NOAA NDBC Ocean Weather** → **⋮** → **Redownload** (or **Update** if an update is available).
3. Choose the **version** you want (e.g. **v1.0.0** or **Default branch**).
4. **Restart Home Assistant**: **Settings** → **System** → **Restart**.

### If you installed manually

1. Download the latest release (or clone the repo) and copy the **`custom_components/noaa_buoy`** folder over your existing one (replace files).
2. **Restart Home Assistant**: **Settings** → **System** → **Restart**.

Your existing config (station IDs, entities, and the Ocean Swim Comfort template) will stay; only the integration code is updated.
