"""Sensor platform for NOAA Buoy integration."""

from __future__ import annotations

from datetime import datetime, timezone

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import NoaaBuoyCoordinator

# Sensor key -> (name, unit, device_class, state_class)
# last_updated = observation timestamp from NDBC data (YY, MM, DD, hh, mm) in UTC
SENSOR_DEFINITIONS: dict[str, tuple[str, str | None, str | None, str | None]] = {
    "last_updated": ("Last Updated", None, SensorDeviceClass.TIMESTAMP, None),
    "wtmp": ("Water Temperature", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, SensorStateClass.MEASUREMENT),
    "atmp": ("Air Temperature", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, SensorStateClass.MEASUREMENT),
    "dewp": ("Dew Point", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, SensorStateClass.MEASUREMENT),
    "pres": ("Pressure", UnitOfPressure.HPA, SensorDeviceClass.PRESSURE, SensorStateClass.MEASUREMENT),
    "wdir": ("Wind Direction", "°", None, SensorStateClass.MEASUREMENT),
    "wspd": ("Wind Speed", UnitOfSpeed.METERS_PER_SECOND, None, SensorStateClass.MEASUREMENT),
    "gst": ("Wind Gust", UnitOfSpeed.METERS_PER_SECOND, None, SensorStateClass.MEASUREMENT),
    "wvht": ("Wave Height", "m", None, SensorStateClass.MEASUREMENT),
    "dpd": ("Dominant Wave Period", "s", None, SensorStateClass.MEASUREMENT),
    "apd": ("Average Wave Period", "s", None, SensorStateClass.MEASUREMENT),
    "mwdd": ("Mean Wave Direction", "°", None, SensorStateClass.MEASUREMENT),
}


def _get_attr(obj: dict | None, key: str):
    """Return value from dict; handle 'mwd' -> 'mwdd' for display name (mwd is reserved-ish)."""
    if obj is None:
        return None
    # NDBC column is MWD; we store as mwd in parsed data
    lookup = "mwdd" if key == "mwdd" else key
    if lookup == "mwdd":
        return obj.get("mwd")
    return obj.get(lookup)


def _observation_timestamp(data: dict | None) -> datetime | None:
    """Build UTC datetime from NDBC observation time (YY, MM, DD, hh, mm)."""
    if data is None:
        return None
    yy = data.get("yy")
    month = data.get("month")
    dd = data.get("dd")
    hh = data.get("hh")
    minute = data.get("minute")
    if yy is None or month is None or dd is None or hh is None or minute is None:
        return None
    # NDBC uses 2-digit year (e.g. 25 = 2025)
    year = 2000 + int(yy) if int(yy) < 100 else int(yy)
    try:
        return datetime(year, int(month), int(dd), int(hh), int(minute), 0, 0, tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return None


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up NOAA Buoy sensors from a config entry."""
    coordinator: NoaaBuoyCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    station_id = coordinator.station_id

    entities = []
    for key, (name, unit, device_class, state_class) in SENSOR_DEFINITIONS.items():
        entities.append(
            NoaaBuoySensor(
                coordinator=coordinator,
                config_entry=config_entry,
                station_id=station_id,
                sensor_key=key,
                name=name,
                unit=unit,
                device_class=device_class,
                state_class=state_class,
            )
        )
    async_add_entities(entities)


class NoaaBuoySensor(CoordinatorEntity[NoaaBuoyCoordinator], SensorEntity):
    """Sensor for a single NOAA buoy measurement."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: NoaaBuoyCoordinator,
        config_entry: ConfigEntry,
        station_id: str,
        sensor_key: str,
        name: str,
        unit: str | None,
        device_class: str | None,
        state_class: str | None,
    ) -> None:
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._station_id = station_id
        self._sensor_key = sensor_key
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        self._attr_unique_id = f"{config_entry.entry_id}_{sensor_key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, config_entry.entry_id)},
            "name": f"NOAA NDBC Ocean Weather {station_id}",
            "manufacturer": "NOAA NDBC",
        }

    @property
    def native_value(self):
        """Return the latest value from the coordinator."""
        if self._sensor_key == "last_updated":
            return _observation_timestamp(self.coordinator.data)
        val = _get_attr(self.coordinator.data, self._sensor_key)
        if val is None:
            return None
        return val
