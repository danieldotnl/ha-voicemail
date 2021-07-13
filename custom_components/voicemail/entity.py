from homeassistant.helpers.entity import Entity

from .const import DOMAIN
from .machine import Machine


class VoicemailEntity(Entity):
    def __init__(self, hass, machine: Machine):
        super().__init__()
        self._machine = machine
        self._hass = hass

    @property
    def device_info(self):
        return {
            "identifiers": {
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, self._machine.name)
            },
            "name": self._machine.name,
            "manufacturer": "HA Voicemail",
        }
