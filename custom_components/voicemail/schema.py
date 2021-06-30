import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .const import ATTR_CONDITION
from .const import ATTR_MESSAGES
from .const import ATTR_SERVICE

MESSAGE_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_SERVICE): cv.service,
        vol.Optional("data"): vol.All(dict, cv.template_complex),
    }
)

SERVICE_RECORD_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_MESSAGES): [MESSAGE_SCHEMA],
    }
)

SERVICE_RECORD_WHEN_SCHEMA = SERVICE_RECORD_SCHEMA.extend(
    {
        vol.Optional(ATTR_CONDITION): cv.template,
    }
)
