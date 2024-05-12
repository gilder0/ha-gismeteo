#  Copyright (c) 2019-2024, Andrey "Limych" Khrolenok <andrey@khrolenok.ru>
#  Creative Commons BY-NC-SA 4.0 International Public License
#  (see LICENSE.md or https://creativecommons.org/licenses/by-nc-sa/4.0/)
"""The Gismeteo component.

For more details about this platform, please refer to the documentation at
https://github.com/Limych/ha-gismeteo/
"""

from functools import cached_property
import logging

from homeassistant.components.weather import WeatherEntity
from homeassistant.config_entries import SOURCE_IMPORT
from homeassistant.const import (
    CONF_NAME,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant

from . import GismeteoDataUpdateCoordinator, _convert_yaml_config, deslugify
from .const import ATTRIBUTION, COORDINATOR, DOMAIN, DOMAIN_YAML
from .entity import GismeteoEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Add a Gismeteo weather entities."""
    entities = []
    if config_entry.source == SOURCE_IMPORT:
        # Setup from configuration.yaml
        for uid, cfg in hass.data[DOMAIN_YAML].items():
            cfg = _convert_yaml_config(cfg)

            location_name = cfg.get(CONF_NAME, deslugify(uid))
            coordinator = hass.data[DOMAIN][uid][COORDINATOR]

            entities.append(GismeteoWeather(coordinator, location_name))

    else:
        # Setup from config entry
        config = config_entry.data.copy()  # type: ConfigType
        config.update(config_entry.options)

        location_name = config[CONF_NAME]
        coordinator = hass.data[DOMAIN][config_entry.entry_id][COORDINATOR]

        entities.append(GismeteoWeather(coordinator, location_name))

    async_add_entities(entities, False)


class GismeteoWeather(GismeteoEntity, WeatherEntity):
    """Implementation of an Gismeteo sensor."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_attribution = ATTRIBUTION
    _attr_native_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_native_pressure_unit = UnitOfPressure.MMHG
    _attr_native_wind_speed_unit = UnitOfSpeed.METERS_PER_SECOND

    def __init__(
        self,
        coordinator: GismeteoDataUpdateCoordinator,
        location_name: str,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, location_name)

        self._attr_unique_id = coordinator.unique_id
        self._attr_translation_placeholders = {
            "location_name": location_name,
        }

    @cached_property
    def condition(self) -> str | None:
        """Return the current condition."""
        return self._gismeteo.condition()

    @cached_property
    def native_temperature(self) -> float | None:
        """Return the temperature in native units."""
        return self._gismeteo.temperature()

    @cached_property
    def native_pressure(self) -> float | None:
        """Return the pressure in native units."""
        return self._gismeteo.pressure()

    @cached_property
    def humidity(self) -> float | None:
        """Return the humidity in %."""
        return self._gismeteo.humidity()

    @cached_property
    def wind_bearing(self) -> float | str | None:
        """Return the wind bearing."""
        return self._gismeteo.wind_bearing()

    @cached_property
    def native_wind_speed(self) -> float | None:
        """Return the wind speed in native units."""
        return self._gismeteo.wind_speed()

    @cached_property
    def cloud_coverage(self) -> float | None:
        """Return the Cloud coverage in %."""
        return self._gismeteo.cloud_coverage()

    @cached_property
    def uv_index(self) -> float | None:
        """Return the UV index."""
        return self._gismeteo.uv_index()

    #
    # @property
    # def forecast(self):
    #     """Return the forecast array."""
    #     return self._gismeteo.forecast()
    #
    # async def async_forecast_daily(self) -> list[Forecast] | None:
    #     """Return the daily forecast in native units."""
    #     raise NotImplementedError
    #
    # async def async_forecast_twice_daily(self) -> list[Forecast] | None:
    #     """Return the daily forecast in native units."""
    #     raise NotImplementedError
    #
    # async def async_forecast_hourly(self) -> list[Forecast] | None:
    #     """Return the hourly forecast in native units."""
    #     raise NotImplementedError
