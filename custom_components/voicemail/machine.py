import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_NAME

_LOGGER = logging.getLogger(__name__)


class Machine:
    def __init__(self, hass: HomeAssistant, config: ConfigEntry):
        self._hass = hass
        self._config = config
        self._messages = []
        self._name = config.data.get(CONF_NAME)
        _LOGGER.debug("Entry %s has data: %s", config.entry_id, config.data)

    def nofMessages(self):
        return len(self._messages)

    async def async_record_when(self, service_call):
        _LOGGER.debug("%s was called with: %s", self._name, service_call)

        condition_template = service_call["condition"]
        if condition_template:
            condition_template.hass = self._hass

        condition: bool = condition_template.async_render(parse_result=False)
        _LOGGER.debug(
            "Condition template %s rendered: %s", condition_template, condition
        )

        messages = service_call["messages"]

        if condition == "True":
            await self.async_record(messages)
        else:
            await self.async_play(messages)

    async def async_record(self, messages):
        for message in messages:
            _LOGGER.info("Message will be recorded: %s", message)
            self._messages.append(message)

    async def _async_play_message(self, message):
        service_id = message["service"].split(".")
        domain = service_id[0]
        name = service_id[1]

        _LOGGER.info("Call service %s with: %s", message["service"], message)

        await self._hass.services.async_call(domain, name, message["data"])

    async def async_play(self):
        while self.nofMessages() > 0:
            message = self._messages.pop(0)
            await self._async_play_message(message)
