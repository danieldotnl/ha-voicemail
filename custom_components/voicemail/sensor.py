"""Sensor platform for HA Voicemail."""
from custom_components.voicemail.const import MACHINE_INSTANCE
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import DOMAIN
from .const import INTEGRATION_NAME
from .const import MESSAGE_COUNT
from .const import SENSOR
from .const import SENSOR_ICON
from .entity import VoicemailEntity
from .helpers import message_update_signal
from .machine import Machine


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    machine: Machine = hass.data[DOMAIN][entry.entry_id][MACHINE_INSTANCE]
    async_add_devices([VoicemailSensor(hass, machine, entry)])


class VoicemailSensor(VoicemailEntity, SensorEntity):
    """voicemail Sensor class."""

    def __init__(self, hass, machine, entry):
        super().__init__(hass, machine._name)
        self._machine = machine
        self._entry = entry

    async def async_on_demand_update(self):
        """Update state."""
        self.async_schedule_update_ha_state(True)

    async def async_added_to_hass(self):
        """Register callbacks."""

        self.async_on_remove(
            async_dispatcher_connect(
                self._hass,
                message_update_signal(self._entry.entry_id),
                self.async_on_demand_update,
            )
        )

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{INTEGRATION_NAME} {self._machine._name} {MESSAGE_COUNT}"

    @property
    def should_poll(self):
        """Return the polling state."""
        return False

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._machine.nofMessages()

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return SENSOR_ICON

    @property
    def device_class(self):
        """Return de device class of the sensor."""
        return "voicemail__custom_device_class"

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{SENSOR}_{self._entry.entry_id}"
