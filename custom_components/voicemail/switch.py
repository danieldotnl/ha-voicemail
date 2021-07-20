"""Switch platform for {{cookiecutter.friendly_name}}."""
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.restore_state import RestoreEntity

from .const import DOMAIN
from .const import INTEGRATION_NAME
from .const import SWITCH
from .const import SWITCH_ICON
from .const import VOICEMAIL_INSTANCE
from .entity import VoicemailEntity
from .voicemail import Voicemail


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    voicemail: Voicemail = hass.data[DOMAIN][entry.entry_id][VOICEMAIL_INSTANCE]
    async_add_devices([VoicemailSwitch(hass, voicemail, entry)])


class VoicemailSwitch(VoicemailEntity, RestoreEntity, SwitchEntity):
    """Voicemail switch class."""

    def __init__(self, hass, voicemail, entry):
        super().__init__(hass, voicemail)
        self._entry = entry
        self._state = False

    def turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the switch."""
        self._state = True
        self.async_write_ha_state()

    def turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the switch."""
        self._state = False
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """Handle entity which will be added."""
        await super().async_added_to_hass()
        state = await self.async_get_last_state()
        if not state:
            return
        self._state = state.state == "on"

    @property
    def name(self):
        """Return the name of the switch."""
        return f"{INTEGRATION_NAME} {self._voicemail.name}"

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self._state

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return SWITCH_ICON

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{SWITCH}_{self._entry.entry_id}"
