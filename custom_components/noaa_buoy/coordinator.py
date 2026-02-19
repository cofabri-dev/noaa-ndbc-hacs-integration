"""DataUpdateCoordinator for NOAA NDBC buoy data."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DEFAULT_UPDATE_INTERVAL, DOMAIN, MISSING_VALUE, NDBC_COLUMNS

NDBC_REALTIME2_URL = "https://www.ndbc.noaa.gov/data/realtime2/{station_id}.txt"

_LOGGER = logging.getLogger(__name__)


def _parse_realtime2_text(text: str) -> dict[str, Any] | None:
    """Parse NDBC realtime2 .txt content; return dict of latest row or None."""
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    data_lines = [line for line in lines if not line.startswith("#")]
    if not data_lines:
        return None
    # First data line is the latest observation
    values = data_lines[0].split()
    if len(values) < len(NDBC_COLUMNS):
        return None
    # Map column names to unique keys (NDBC has MM=month and mm=minute; both would become "mm")
    COLUMN_KEYS = (
        "yy", "month", "dd", "hh", "minute",  # YY MM DD hh mm
        "wdir", "wspd", "gst", "wvht", "dpd", "apd", "mwd",
        "pres", "atmp", "wtmp", "dewp", "vis", "ptdy", "tide",
    )
    result: dict[str, Any] = {}
    for i, col in enumerate(NDBC_COLUMNS):
        if i >= len(values) or i >= len(COLUMN_KEYS):
            break
        raw = values[i]
        key = COLUMN_KEYS[i]
        if raw == MISSING_VALUE:
            result[key] = None
            continue
        try:
            if col in ("WDIR", "MWD", "YY", "MM", "DD", "hh", "mm"):
                result[key] = int(float(raw))
            else:
                result[key] = float(raw)
        except (ValueError, TypeError):
            result[key] = raw
    return result


async def fetch_station_data(session, station_id: str) -> dict[str, Any] | None:
    """Fetch and parse one station's realtime2 data. Used by coordinator and config_flow."""
    url = NDBC_REALTIME2_URL.format(station_id=station_id.strip())
    try:
        async with session.get(url, timeout=10) as resp:
            if resp.status != 200:
                return None
            text = await resp.text()
    except Exception as e:
        _LOGGER.debug("NDBC fetch failed for %s: %s", station_id, e)
        raise
    return _parse_realtime2_text(text)


class NoaaBuoyCoordinator(DataUpdateCoordinator[dict[str, Any] | None]):
    """Coordinator for a single NOAA buoy station."""

    def __init__(self, hass: HomeAssistant, station_id: str) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{station_id}",
            update_interval=timedelta(minutes=DEFAULT_UPDATE_INTERVAL),
        )
        self.station_id = station_id.strip()

    async def _async_update_data(self) -> dict[str, Any] | None:
        session = async_get_clientsession(self.hass)
        try:
            new_data = await fetch_station_data(session, self.station_id)
            if new_data is None:
                raise UpdateFailed("No data in NDBC response")
            # Keep last reported value for any param not in this update (NDBC sometimes omits some params)
            previous = self.data or {}
            merged = dict(previous)
            for key, value in new_data.items():
                if value is not None:
                    merged[key] = value
            return merged
        except Exception as e:
            raise UpdateFailed(f"Failed to fetch NDBC data: {e}") from e
