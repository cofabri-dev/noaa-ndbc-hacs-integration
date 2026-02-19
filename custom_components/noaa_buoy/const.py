"""Constants for the NOAA Buoy integration."""

DOMAIN = "noaa_buoy"

CONF_STATION_ID = "station_id"

# NDBC realtime2 data is typically updated hourly (~25 min after the hour)
DEFAULT_UPDATE_INTERVAL = 30  # minutes

# Standard meteorological columns (order matches NDBC .txt format)
# YY MM DD hh mm WDIR WSPD GST WVHT DPD APD MWD PRES ATMP WTMP DEWP VIS PTDY TIDE
NDBC_COLUMNS = [
    "YY", "MM", "DD", "hh", "mm",
    "WDIR", "WSPD", "GST", "WVHT", "DPD", "APD", "MWD",
    "PRES", "ATMP", "WTMP", "DEWP", "VIS", "PTDY", "TIDE",
]
MISSING_VALUE = "MM"
