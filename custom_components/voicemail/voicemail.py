import logging

from homeassistant.const import CONF_NAME
from homeassistant.helpers import template

from .const import FINISH_TEMPLATE
from .const import INTEGRATION_NAME
from .const import START_TEMPLATE
from .const import SWITCH
from .store import MessageStore

_LOGGER = logging.getLogger(__name__)


class Voicemail:
    def __init__(self, hass, entry):
        self._hass = hass
        self._store = MessageStore(hass, entry.entry_id)
        self._entry = entry
        self.name = entry.data.get(CONF_NAME)

    def message_count(self):
        return len(self._store)

    def peek_all(self):
        return self._store.peek_all()

    async def async_setup(self):
        await self._store.async_load_messages()

    async def async_record(self, messages):
        _LOGGER.debug("Message will be recorded: %s", messages)
        await self._store.append_list(messages)

    async def async_record_when(self, condition_template, messages):
        if condition_template:
            # record when condition is met
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

        if condition == "True" or condition is True:
            await self.async_record(messages)
        else:
            await self.async_play(messages)

    async def async_play(self, messages):
        for message in messages:
            data = _create_template(message.data)

            print("Data %s", data)
            template.attach(self._hass, data)
            result = template.render_complex(data)
            print("Parsed data: %s", result)

            domain, service = message.service.split(".", 1)
            _LOGGER.debug("Call service %s with: %s", message.service, result)
            await self._hass.services.async_call(domain, service, result)

    async def async_play_all(self):
        messages = await self._store.pop_all()
        _LOGGER.debug("Playing all %s messages", len(messages))
        await self.async_play(messages)


def _create_template(data):
    if isinstance(data, dict):
        return {k: _create_template(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [_create_template(i) for i in data]
    else:
        data = data.replace(START_TEMPLATE, "{{")
        data = data.replace(FINISH_TEMPLATE, "}}")
        if template.is_template_string(data):
            return template.Template(data)
        return data
