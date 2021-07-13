"""Constants for HA Voicemail."""
# Base component constants
INTEGRATION_NAME = "Voicemail"
DOMAIN = "voicemail"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"

ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"
ISSUE_URL = "https://github.com/danieldotnl/ha-voicemail/issues"

MACHINE_INSTANCE = "machine"
MESSAGE_UPDATE_SIGNAL = "voicemail_update"

# Icons
SENSOR_ICON = "mdi:format-list-numbered"
SWITCH_ICON = "mdi:voicemail"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
BINARY_SENSOR = "binary_sensor"
SENSOR = "sensor"
SWITCH = "switch"
# PLATFORMS = [BINARY_SENSOR, SENSOR, SWITCH]
PLATFORMS = [SENSOR, SWITCH]

# Configuration and options
CONF_ENABLED = "enabled"
CONF_NAME = "name"

# Defaults
MESSAGES = "messages"


# Services
ATTR_CONDITION = "condition"
ATTR_MESSAGES = "messages"
ATTR_SERVICE = "service"
