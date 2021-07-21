import logging

from homeassistant.components.select import SelectEntity
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import DOMAIN
from .const import VOICEMAIL_INSTANCE
from .entity import VoicemailEntity
from .helpers import message_update_signal
from .voicemail import Voicemail

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    voicemail: Voicemail = hass.data[DOMAIN][entry.entry_id][VOICEMAIL_INSTANCE]
    async_add_devices([VoicemailSelect(hass, voicemail, entry)])


class VoicemailSelect(VoicemailEntity, SelectEntity):
    def __init__(self, hass, voicemail, entry):
        super().__init__(hass, voicemail)
        self._entry = entry
        self._attr_options = []
        self._attr_current_option = None

    async def async_select_option(self, option: str) -> None:
        _LOGGER.debug("Option chosen from select: %s", option)
        self._attr_current_option = option

    async def _async_refresh(self):
        self._options = []
        for message in self._voicemail.peek_all():
            _LOGGER.debug("Looping through messages with name: %s", message.name)
            self._options.append(message.name)
        self._attr_options = self._options
        if not self._attr_current_option and len(self._attr_options) > 0:
            self._attr_current_option = self._attr_options[0]
        elif self._attr_current_option not in self._attr_options:
            self._attr_current_option = None

        self.async_schedule_update_ha_state(True)

    async def async_added_to_hass(self):
        """Register callbacks."""

        self.async_on_remove(
            async_dispatcher_connect(
                self._hass,
                message_update_signal(self._entry.entry_id),
                self._async_refresh,
            )
        )
        await self._async_refresh()

    @property
    def should_poll(self):
        """Return the polling state."""
        return False
