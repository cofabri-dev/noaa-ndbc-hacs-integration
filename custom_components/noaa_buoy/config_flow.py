"""Config flow for NOAA Buoy integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_STATION_ID, DOMAIN
from .coordinator import fetch_station_data

_LOGGER = logging.getLogger(__name__)


async def _validate_station(hass: HomeAssistant, station_id: str) -> str | None:
    """Validate station ID by fetching realtime2 data. Returns error key or None."""
    station_id = (station_id or "").strip()
    if not station_id:
        return "invalid_station"
    session = async_get_clientsession(hass)
    try:
        data = await fetch_station_data(session, station_id)
        if data is None:
            return "invalid_station"
        return None
    except Exception:
        return "cannot_connect"


class NoaaBuoyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for NOAA Buoy."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            station_id = (user_input.get(CONF_STATION_ID) or "").strip()
            if not station_id:
                errors[CONF_STATION_ID] = "invalid_station"
            else:
                error = await _validate_station(self.hass, station_id)
                if error:
                    errors["base"] = error
                else:
                    await self.async_set_unique_id(station_id.lower())
                    self._abort_if_unique_id_configured()
                    return self.async_create_entry(
                        title=station_id,
                        data={CONF_STATION_ID: station_id},
                    )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_STATION_ID, default=""): str,
                }
            ),
            errors=errors,
            description_placeholders={
                "station_list_url": "https://ndbc.noaa.gov/to_station.shtml",
                "map_url": "https://ndbc.noaa.gov/obs.shtml",
            },
        )
