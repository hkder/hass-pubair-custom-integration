"""Support for Met.no weather service."""
import logging

import voluptuous as vol

from homeassistant.components.air_quality import AirQualityEntity

from homeassistant.config_entries import SOURCE_IMPORT
from homeassistant.const import (
    CONF_ELEVATION,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_NAME,
    LENGTH_INCHES,
    LENGTH_KILOMETERS,
    LENGTH_MILES,
    LENGTH_MILLIMETERS,
    PRESSURE_HPA,
    PRESSURE_INHG,
    TEMP_CELSIUS,
)
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    CONF_UMDNAME,
)

_LOGGER = logging.getLogger(__name__)

ATTRIBUTION = (
    "RealTime Air Pollution Levels from apis.data.go.kr delivered by Air Korea."
)
DEFAULT_NAME = "Air Korea Open API"


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add a weather entity from a config_entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities(
        [
            PubAirWeather(coordinator, config_entry.data, True),
        ]
    )


class PubAirWeather(CoordinatorEntity, AirQualityEntity):
    """Implementation of a Met.no weather condition."""

    def __init__(self, coordinator, config, hourly):
        """Initialise the platform with a data instance and site."""
        super().__init__(coordinator)
        self._config = config
        self._hourly = hourly
        self._icon = "mdi:blur"

    @property
    def unique_id(self):
        """Return unique ID."""
        name_appendix = ""
        if self._hourly:
            name_appendix = "-hourly"

        return f"{self._config[CONF_UMDNAME]}{name_appendix}"

    @property
    def name(self):
        """Return the name of the sensor."""
        name = self._config.get(CONF_UMDNAME)
        name_appendix = ""
        if self._hourly:
            name_appendix = " Hourly"

        if name is not None:
            return f"{name}{name_appendix}"

        return f"{DEFAULT_NAME}{name_appendix}"

    @property
    def icon(self):
        """Return the icon."""
        return self._icon

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return if the entity should be enabled when first added to the entity registry."""
        return self._hourly

    @property
    def particulate_matter_2_5(self):
        pm2d5 = self.coordinator.data.current_airpollution_data["pm25Value"]
        return float(pm2d5)

    @property
    def particulate_matter_10(self):
        pm10 = self.coordinator.data.current_airpollution_data["pm10Value"]
        return float(pm10)

    @property
    def attribution(self):
        """Return the attribution."""
        return ATTRIBUTION

    @property
    def device_info(self):
        """Device info."""
        return {
            "identifiers": {(DOMAIN,)},
            "manufacturer": "Air Korea",
            "model": "Real Time Air Pollution",
            "default_name": "Real Time Air Pollution",
            "entry_type": "service",
        }
