from .const import DOMAIN


class VoicemailEntity:
    def __init__(self, name):
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
