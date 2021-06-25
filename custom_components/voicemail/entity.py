from homeassistant.helpers.entity import Entity

from .const import DOMAIN


class VoicemailEntity(Entity):
    def __init__(self, name):
        super().__init__()
        self._name = name

    @property
    def device_info(self):
        return {
            "identifiers": {
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, self._name)
            },
            "name": self.name,
            "manufacturer": "HA Voicemail",
        }
