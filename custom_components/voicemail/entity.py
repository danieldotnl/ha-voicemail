"""VoicemailEntity class"""
from homeassistant.components.sensor import SensorEntity


class VoicemailEntity(SensorEntity):
    def __init__(self, machine, config_entry):
        self._config_entry = config_entry
        self._machine = machine

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self._config_entry.entry_id
