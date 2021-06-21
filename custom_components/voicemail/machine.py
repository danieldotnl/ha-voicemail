import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)


class Machine:
    def __init__(self, hass: HomeAssistant, config: ConfigEntry):
        self._hass = hass
        self._config = config

    async def async_record_when(self, condition, data):
        _LOGGER.debug("Service was called with: %s", data)

        split = data["service"].split(".")
        domain = split[0]
        name = split[1]

        await self._hass.services.async_call(domain, name, data["data"])
