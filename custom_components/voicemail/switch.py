"""Switch platform for {{cookiecutter.friendly_name}}."""
from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN
from .const import INTEGRATION_NAME
from .const import MACHINE_INSTANCE
from .const import SWITCH
from .const import SWITCH_ICON
from .machine import Machine


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    machine: Machine = hass.data[DOMAIN][entry.entry_id][MACHINE_INSTANCE]
    async_add_devices([VoicemailSwitch(machine, entry)])


class VoicemailSwitch(SwitchEntity):
    """Voicemail switch class."""

    def __init__(self, machine, entry):
        self._machine = machine
        self._entry = entry
        self._state = False

    def turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the switch."""
        self._state = True

    def turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the switch."""
        self._state = False

    @property
    def name(self):
        """Return the name of the switch."""
        return f"{INTEGRATION_NAME} {self._machine._name}"

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
