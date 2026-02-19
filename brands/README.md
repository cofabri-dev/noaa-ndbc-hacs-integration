# Brand assets (NOAA NDBC Ocean Weather)

This folder contains icon and logo assets for the **noaa_buoy** integration.

- **icon.png** – Square icon for the integration (e.g. in Settings → Integrations and in HACS).
- **logo.png** – Optional logo for the integration.

## Why it says "Icon Not Available" in HA / HACS

Home Assistant and HACS **only** load integration icons from [brands.home-assistant.io](https://brands.home-assistant.io/), which is populated from the [home-assistant/brands](https://github.com/home-assistant/brands) repository. Until **noaa_buoy** is added there, the integration will show "Icon Not Available" in Settings → Integrations and in HACS. Adding an icon to this repo alone is not enough—you must submit it to **home-assistant/brands**.

## How to get the icon to show

1. Fork the [home-assistant/brands](https://github.com/home-assistant/brands) repository.
2. In your fork, create the folder **`custom_integrations/noaa_buoy/`**.
3. Copy **`icon.png`** (and optionally **`logo.png`**) from this repo’s **`brands/noaa_buoy/`** into **`custom_integrations/noaa_buoy/`** in the brands repo.
4. Open a pull request to [home-assistant/brands](https://github.com/home-assistant/brands) with the new folder and file(s).
5. After the PR is merged, the integration will use `https://brands.home-assistant.io/noaa_buoy/icon.png` and the icon will appear in Home Assistant and HACS.

The folder name **noaa_buoy** must match the integration **domain** in `manifest.json`.

## Official NOAA emblem

These assets are integration branding for *NOAA NDBC Ocean Weather* and are not the official NOAA emblem. For the official emblem and usage rules, see [NOAA’s emblem and logo page](https://www.noaa.gov/office-of-communication/about-noaa-emblem-and-logo).
