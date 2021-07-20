import json
import logging
from datetime import datetime
from json.encoder import JSONEncoder

from .const import INTEGRATION_NAME
from .helpers import message_update_signal

STORAGE_VERSION = 1
_LOGGER = logging.getLogger(__name__)


class MessageStore:
    def __init__(self, hass, entry_id):
        self._hass = hass
        self._entry_id = entry_id
        self._messages = []

        key = f"{INTEGRATION_NAME}_{self._entry_id}"
        self._store = hass.helpers.storage.Store(
            STORAGE_VERSION, key, encoder=MessageEncoder
        )

    def __len__(self):
        return len(self._messages)

    async def async_load_messages(self):
        messages = await self._store.async_load()
        if messages:
            self._messages = messages
        self._hass.helpers.dispatcher.dispatcher_send(
            message_update_signal(self._entry_id)
        )

    async def _async_save_messages(self):
        # _LOGGER.debug("SDFS: %s", vars(self._messages[0]))json.dumps(employee, indent=4, cls=EmployeeEncoder)
        _LOGGER.debug(
            "LOGGING data is: %s", json.dumps(self._messages, cls=MessageEncoder)
        )
        await self._store.async_save(self._messages)

    # async def append(self, message: Message):
    #     self._messages.append(message)
    #     await self._async_save_messages()
    #     self._hass.helpers.dispatcher.dispatcher_send(
    #         message_update_signal(self._entry_id)
    #     )

    async def append_list(self, messages):
        self._messages.extend(messages)
        await self._async_save_messages()
        self._hass.helpers.dispatcher.dispatcher_send(
            message_update_signal(self._entry_id)
        )

    async def pop(self, index: int = 0):
        message = self._messages.pop(index)
        await self._async_save_messages()
        self._hass.helpers.dispatcher.dispatcher_send(
            message_update_signal(self._entry_id)
        )
        return message

    async def pop_all(self):
        result, self._messages = self._messages, []
        await self._async_save_messages()
        self._hass.helpers.dispatcher.dispatcher_send(
            message_update_signal(self._entry_id)
        )
        return result


class MessageEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return o.__dict__
