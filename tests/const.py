"""Constants for tests."""

from custom_components.gismeteo.const import CONF_PLATFORM_FORMAT
from homeassistant.const import (
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_NAME,
    CONF_SENSORS,
    Platform,
)

FAKE_NAME = "Home"
FAKE_UNIQUE_ID = "test_id"
FAKE_LATITUDE = 55.55
FAKE_LONGITUDE = 122.12

FAKE_CONFIG = {
    CONF_NAME: FAKE_NAME,
    CONF_LATITUDE: FAKE_LATITUDE,
    CONF_LONGITUDE: FAKE_LONGITUDE,
}

FAKE_CONFIG_OPTIONS = {
    CONF_PLATFORM_FORMAT.format(Platform.SENSOR): True,
}

FAKE_CONFIG_YAML = {
    "home": {
        CONF_NAME: FAKE_NAME,
        CONF_LATITUDE: FAKE_LATITUDE,
        CONF_LONGITUDE: FAKE_LONGITUDE,
        CONF_SENSORS: {},
    },
}
