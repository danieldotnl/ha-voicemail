from homeassistant.helpers.entity import Entity

from .const import DOMAIN
from .voicemail import Voicemail


class VoicemailEntity(Entity):
    def __init__(self, hass, voicemail: Voicemail):
        super().__init__()
        self._voicemail = voicemail
        self._hass = hass

    @property
    def device_info(self):
        return {
            "identifiers": {
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, self._voicemail.name)
            },
            "name": self._voicemail.name,
            "manufacturer": "HA Voicemail",
        }
