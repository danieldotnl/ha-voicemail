"""Sensor platform for HA Voicemail."""
from custom_components.voicemail.const import MACHINE_INSTANCE

from .const import DOMAIN
from .const import ICON
from .const import MESSAGE_COUNT
from .entity import VoicemailEntity
from .machine import Machine


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    machine: Machine = hass.data[DOMAIN][entry.entry_id][MACHINE_INSTANCE]
    async_add_devices([VoicemailSensor(machine, entry)])


class VoicemailSensor(VoicemailEntity):
    """voicemail Sensor class."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._machine._name} {MESSAGE_COUNT}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._machine.nofMessages()

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON

    @property
    def device_class(self):
        """Return de device class of the sensor."""
        return "voicemail__custom_device_class"
