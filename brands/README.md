# Brand assets (NOAA NDBC Ocean Weather)

This folder contains icon and logo assets for the **noaa_buoy** integration.

- **icon.png** – Square icon for the integration (e.g. in Settings → Integrations).
- **logo.png** – Logo for the integration.

## Showing the logo in Home Assistant

Home Assistant loads integration icons from [brands.home-assistant.io](https://brands.home-assistant.io/), which is populated from the [home-assistant/brands](https://github.com/home-assistant/brands) repository.

To have this integration’s icon and logo appear in Home Assistant:

1. Open a pull request to [home-assistant/brands](https://github.com/home-assistant/brands).
2. Add the contents of `brands/noaa_buoy/` into **`custom_integrations/noaa_buoy/`** in that repo (so `icon.png` and `logo.png` are in `custom_integrations/noaa_buoy/`).
3. After the PR is merged, the integration will use `https://brands.home-assistant.io/noaa_buoy/icon.png` and `.../logo.png` in the UI.

The `noaa_buoy` folder name must match the integration **domain** in `manifest.json`.

## Official NOAA emblem

These assets are integration branding for *NOAA NDBC Ocean Weather* and are not the official NOAA emblem. For the official emblem and usage rules, see [NOAA’s emblem and logo page](https://www.noaa.gov/office-of-communication/about-noaa-emblem-and-logo).
