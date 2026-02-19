# Ocean Notifications (multi-station) example

This example automation uses NOAA NDBC Ocean Weather sensors plus an [Ocean Swim Comfort](OCEAN_SWIM_COMFORT.md) template sensor to:

- Track swim comfort and weather conditions
- Derive simple flags (rip risk, rough ocean, glass calm, etc.) from wave height, period, and direction
- Compare water temperature to 24 hours ago
- Send notifications when comfort changes or on a daily schedule

The example is written for **two stations** (primary and fallback). You can use a single station by simplifying the variables, or add more fallbacks.

**Before using:** Replace all placeholder entity IDs and notification targets with your own. Use **Developer Tools** → **States** to find your sensor and weather entity IDs.

---

## Why use more than one station?

Configuring a second (or third) NDBC station as a fallback is useful because:

- **Buoy or station can be offline** — Moorings fail, power is lost, or a station is temporarily removed. If your automation depends on one station, it will see "unavailable" until that station returns.
- **Gaps in reporting** — A station might skip updates or stop reporting for a while. A nearby C-MAN or buoy can fill in so your notifications and comfort logic still have data.
- **Not all parameters in every reading** — NDBC updates often include only a subset of parameters (e.g. wind and waves but no water temperature in a given hour). The integration keeps the last reported value for each parameter, but if the primary station hasn’t reported water temperature in a long time, a fallback station that does report it can give you a usable value.

In this example, `use_station` switches between a primary and fallback set of sensors. You can set it from a helper, time of day, or condition (e.g. use fallback when primary’s water temperature is unavailable).

---

## Required setup

1. **NOAA NDBC Ocean Weather** integration configured for one or more stations (e.g. buoy + C-MAN).
2. **Ocean Swim Comfort** template sensor from [OCEAN_SWIM_COMFORT.md](OCEAN_SWIM_COMFORT.md) (entity: `sensor.ocean_swim_comfort` or your chosen ID).
3. **Weather** entity for your location (e.g. `weather.home` — replace `weather.home` in the automation with your actual weather entity).
4. **Helpers** (create in **Settings** → **Devices & services** → **Helpers**):
   - **Input Number:** `input_number.ocean_water_temp_24h_ago` — stores water temp 24h ago (no UI needed).
   - **Input Text:** `input_text.ocean_alert_flags` — optional; stores last alert flags for comparison.

---

## Example automation YAML

Use this in **Settings** → **Automations & Scenes** → **Create Automation** → **Edit in YAML**, or paste into a new automation and adapt.

- Replace `sensor.noaa_ndbc_ocean_weather_41122_*` and `sensor.noaa_ndbc_ocean_weather_41002_*` with your NDBC sensor entity IDs (e.g. from stations you configured). The example uses **41122** as primary and **41002** as fallback; use your own station IDs.
- Replace `weather.home` with your weather entity (e.g. `weather.forecast_home`).
- Replace `notify.notify` with your preferred notification target (e.g. `notify.mobile_app_phone`, `notify.all_devices`).

```yaml
alias: Ocean Notifications
description: Swim conditions and comfort alerts from NOAA NDBC + weather (multi-station)
trigger:
  - platform: state
    entity_id:
      - sensor.ocean_swim_comfort
    id: comfort_changed
  - platform: time
    at: "08:00:00"
    id: daily_weekday_time
  - platform: time
    at: "09:00:00"
    id: daily_weekend_time
  - platform: time
    at: "07:00:00"
    id: baseline_24h
action:
  - variables:
      # Primary vs fallback: use your own station entity IDs (41122 / 41002 are placeholders)
      use_station: "primary"
      station_label: >-
        {{ 'Primary (41122)' if use_station == 'primary' else 'Fallback (41002)' }}
      air: >-
        {{ states('sensor.noaa_ndbc_ocean_weather_41122_air_temperature') | float(0) * 9/5 + 32 | round(0) | int
           if use_station == 'primary' else
           states('sensor.noaa_ndbc_ocean_weather_41002_air_temperature') | float(0) * 9/5 + 32 | round(0) | int }}
      water: >-
        {{ states('sensor.noaa_ndbc_ocean_weather_41122_water_temperature') | float(0) * 9/5 + 32 | round(1)
           if use_station == 'primary' else
           states('sensor.noaa_ndbc_ocean_weather_41002_water_temperature') | float(0) * 9/5 + 32 | round(1) }}
      wave_h: |-
        {% if use_station == 'primary' %}
          {{ states('sensor.noaa_ndbc_ocean_weather_41122_wave_height') | float(0) }}
        {% else %}
          {{ states('sensor.noaa_ndbc_ocean_weather_41002_wave_height') | float(0) }}
        {% endif %}
      dom_p: |-
        {% if use_station == 'primary' %}
          {{ states('sensor.noaa_ndbc_ocean_weather_41122_dominant_wave_period') | float(0) }}
        {% else %}
          {{ states('sensor.noaa_ndbc_ocean_weather_41122_average_wave_period') | float(0) }}
        {% endif %}
      wave_dir: |-
        {% if use_station == 'primary' %}
          {{ states('sensor.noaa_ndbc_ocean_weather_41122_mean_wave_direction') | float(0) }}
        {% else %}
          {{ states('sensor.noaa_ndbc_ocean_weather_41002_mean_wave_direction') | float(0) }}
        {% endif %}
      comfort: "{{ states('sensor.ocean_swim_comfort') }}"
      wx_state: "{{ states('weather.home') }}"
      wx_temp: >-
        {{ state_attr('weather.home','temperature') | float(0) | round(0) | int }}
      wx_wind: >-
        {{ state_attr('weather.home','wind_speed') | float(0) | round(0) | int }}
      wx_uv: "{{ state_attr('weather.home','uv_index') | float(0) }}"
      forecast_list: "{{ state_attr('weather.home','forecast') | default([], true) }}"
      f0: |-
        {% set fl = forecast_list %}
        {% if fl is iterable and (fl | count) > 0 %}
          {{ fl | first }}
        {% else %}
          {{ dict() }}
        {% endif %}
      wx_pop: "{{ f0.get('precipitation_probability', 0) | float(0) | round(0) | int }}"
      wx_rain: "{{ f0.get('precipitation', 0) | float(0) }}"
      comfort_ok: "{{ comfort in ['Comfortable','Great','Perfect','Warm','Bathwater'] }}"
      weather_ok: |-
        {{
          wx_state not in ['rainy','pouring','lightning','lightning-rainy','snowy','snowy-rainy','hail','exceptional']
          and wx_wind <= 18
          and wx_pop <= 35
          and wx_rain <= 1.0
        }}
      recommendation: |-
        {% if comfort_ok and weather_ok %}
          ✅ Good swim window
        {% else %}
          ❌ Not recommended
        {% endif %}
      wx_summary: >-
        {{ wx_state | replace('_',' ') | title }} · {{ wx_temp }}°F · Wind {{ wx_wind }}mph · Rain {{ wx_pop }}%
      onshore_swell: "{{ wave_dir >= 45 and wave_dir <= 135 }}"
      rip_risk: "{{ wave_h >= 1.2 and dom_p >= 8 and onshore_swell }}"
      rough_ocean: "{{ wave_h >= 1.5 }}"
      glass_calm: "{{ wave_h <= 0.6 and dom_p >= 7 and wx_wind <= 10 }}"
      onshore_break: "{{ onshore_swell and wave_h >= 1.0 }}"
      water_24h_ago: "{{ states('input_number.ocean_water_temp_24h_ago') | float(0) }}"
      water_delta_24h: "{{ (water | float(0) - water_24h_ago | float(0)) | round(0) | int }}"
      water_drop_24h: "{{ water_24h_ago > 0 and water_delta_24h <= -2 }}"
      water_rise_24h: "{{ water_24h_ago > 0 and water_delta_24h >= 2 }}"
      high_uv_warm_water: "{{ wx_uv >= 8 and (water | float(0)) >= 75 }}"
      alert_flags: |-
        {{
          [
            'RIP' if rip_risk else none,
            'ROUGH' if rough_ocean else none,
            'GLASS' if glass_calm else none,
            'ONSHORE' if onshore_break else none,
            'DROP' if water_drop_24h else none,
            'RISE' if water_rise_24h else none,
            'UV' if high_uv_warm_water else none
          ]
          | reject('equalto', none)
          | list
          | join(',')
          if (
            rip_risk or rough_ocean or glass_calm or
            onshore_break or water_drop_24h or
            water_rise_24h or high_uv_warm_water
          )
          else 'NONE'
        }}
      last_flags: "{{ states('input_text.ocean_alert_flags') | default('NONE', true) }}"
      alerts_human: |-
        {% if alert_flags == 'NONE' %}
          No special advisories
        {% else %}
          {{ alert_flags | replace(',', ' · ') }}
        {% endif %}
  - choose:
      - conditions:
          - condition: trigger
            id: baseline_24h
        sequence:
          - action: input_number.set_value
            target:
              entity_id: input_number.ocean_water_temp_24h_ago
            data:
              value: "{{ water }}"
      - conditions:
          - condition: trigger
            id: comfort_changed
        sequence:
          - action: notify.notify
            data:
              title: "🌊 Swim status changed"
              message: >-
                {{ recommendation }} — {{ comfort }}. Air {{ air }}°F / Water {{ water }}°F.
                Wx: {{ wx_summary }}. Src: {{ station_label }}.
      - conditions:
          - condition: trigger
            id:
              - daily_weekday_time
              - daily_weekend_time
        sequence:
          - action: input_text.set_value
            target:
              entity_id: input_text.ocean_alert_flags
            data:
              value: "{{ alert_flags }}"
          - action: notify.notify
            data:
              title: "Ocean conditions"
              message: >-
                {{ recommendation }} — {{ comfort }}. Air {{ air }}°F / Water {{ water }}°F.
                {{ alerts_human }}. Wx: {{ wx_summary }}.
```

---

## Customization

- **Stations:** Replace **41122** and **41002** with your NDBC station IDs (or the exact entity IDs from Developer Tools). For a single station, remove the `if use_station` branches and use one set of sensors everywhere.
- **Choosing primary vs fallback:** You can set `use_station` from an `input_select`, or use a condition (e.g. use fallback when primary’s water temperature is `unavailable`).
- **Comfort bands:** The `comfort_ok` list should match the states from your [Ocean Swim Comfort](OCEAN_SWIM_COMFORT.md) template (e.g. add or remove `'Bathwater'`, `'Great'`, etc.).
- **Thresholds:** Adjust `wave_h`, `dom_p`, `wave_dir`, `wx_wind`, `wx_pop`, `wx_rain`, and `wx_uv` limits to your preference.
- **Notification target:** Use a specific device (e.g. `notify.mobile_app_phone`) or a notify group instead of `notify.notify`.
</think>
Fixing a copy-paste error: fallback `dom_p` used 41122 for average_wave_period; it should use 41002.
<｜tool▁calls▁begin｜><｜tool▁call▁begin｜>
StrReplace