import json
import logging
from datetime import datetime
from json.encoder import JSONEncoder

from .const import INTEGRATION_NAME
from .helpers import json_messages_to_dict
from .helpers import message_update_signal

STORAGE_VERSION = 1
_LOGGER = logging.getLogger(__name__)


class MessageStore:
    def __init__(self, hass, entry_id):
        self._hass = hass
        self._entry_id = entry_id
        self._messages = {}

        key = f"{INTEGRATION_NAME}_{self._entry_id}"
        self._store = hass.helpers.storage.Store(
            STORAGE_VERSION, key, encoder=MessageEncoder
        )

    def __len__(self):
        return len(self._messages)

    def peek_all(self):
        return list(self._messages.values().sort(key=lambda m: m.created))

    async def async_load_messages(self):
        json_messages = await self._store.async_load()
        if json_messages:
            self._messages = json_messages_to_dict(json_messages.values())
        self._hass.helpers.dispatcher.dispatcher_send(
            message_update_signal(self._entry_id)
        )

    async def _async_save_messages(self):
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
        for message in messages:
            self._append(message)

        await self._async_save_messages()
        self._hass.helpers.dispatcher.dispatcher_send(
            message_update_signal(self._entry_id)
        )

    def _append(self, message):
        self._messages[message.code] = message

    async def pop(self, index: int = 0):
        message = self._messages.pop(index)
        await self._async_save_messages()
        self._hass.helpers.dispatcher.dispatcher_send(
            message_update_signal(self._entry_id)
        )
        return message

    async def pop_all(self):
        result, self._messages = self._messages, {}
        await self._async_save_messages()
        self._hass.helpers.dispatcher.dispatcher_send(
            message_update_signal(self._entry_id)
        )
        return list(result.values().sort(key=lambda m: m.created))


class MessageEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return o.__dict__
