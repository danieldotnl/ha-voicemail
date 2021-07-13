import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import ATTR_CONDITION
from .const import CONF_NAME
from .const import INTEGRATION_NAME
from .const import SWITCH
from .helpers import message_update_signal

_LOGGER = logging.getLogger(__name__)
STORAGE_VERSION = 1


class Machine:
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self._hass = hass
        self._entry = entry
        self._messages = []
        self.name = entry.data.get(CONF_NAME)
        _LOGGER.debug("Entry %s has data: %s", entry.entry_id, entry.data)

        key = f"{INTEGRATION_NAME}_{entry.entry_id}"
        self._store = hass.helpers.storage.Store(STORAGE_VERSION, key)

    def nofMessages(self):
        return len(self._messages)

    async def async_save_messages(self):
        await self._store.async_save(self._messages)

    async def async_load_messages(self):
        messages = await self._store.async_load()
        if messages:
            self._messages = messages
        self._hass.helpers.dispatcher.dispatcher_send(
            message_update_signal(self._entry.entry_id)
        )

    async def async_record(self, service_call):
        _LOGGER.debug("%s was called with: %s", self.name, service_call)
        messages = service_call["messages"]
        await self._async_record(messages)

    async def async_record_when(self, service_call):
        _LOGGER.debug("%s was called with: %s", self.name, service_call)

        condition_template = service_call.get(ATTR_CONDITION)
        if condition_template:
            condition_template.hass = self._hass
            condition: bool = condition_template.async_render(parse_result=False)
            _LOGGER.debug(
                "Condition template %s rendered: %s", condition_template, condition
            )

        else:
            # record when switch.voicemail is switched on
            condition: bool = (
                self._hass.states.get(f"{SWITCH}.{INTEGRATION_NAME}_{self.name}").state
                == "on"
            )
            _LOGGER.debug("Condition based on switch: %s", condition)

        messages = service_call["messages"]

        if condition == "True" or condition is True:
            await self._async_record(messages)
        else:
            await self._async_play_messages(messages)

    async def _async_record(self, messages):
        for message in messages:
            _LOGGER.info("Message will be recorded: %s", message)
            self._messages.append(message)
        await self.async_save_messages()
        self._hass.helpers.dispatcher.dispatcher_send(
            message_update_signal(self._entry.entry_id)
        )

    async def _async_play_message(self, message):
        service_id = message["service"].split(".")
        domain = service_id[0]
        name = service_id[1]

        _LOGGER.info("Call service %s with: %s", message["service"], message)

        await self._hass.services.async_call(domain, name, message.get("data"))

    async def async_play(self):
        while self.nofMessages() > 0:
            message = self._messages.pop(0)
            await self._async_play_message(message)
        await self.async_save_messages()
        self._hass.helpers.dispatcher.dispatcher_send(
            message_update_signal(self._entry.entry_id)
        )

    async def _async_play_messages(self, messages):
        for message in messages:
            await self._async_play_message(message)
