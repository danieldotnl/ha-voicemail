"""
Custom integration to integrate HA Voicemail with Home Assistant.

For more details about this integration, please refer to
https://github.com/danieldotnl/ha-voicemail
"""
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config
from homeassistant.core import HomeAssistant

from .const import ATTR_CONDITION
from .const import CONF_NAME
from .const import DOMAIN
from .const import PLATFORMS
from .const import VOICEMAIL_INSTANCE
from .helpers import json_messages_to_list
from .schema import SERVICE_RECORD_SCHEMA
from .schema import SERVICE_RECORD_WHEN_SCHEMA
from .voicemail import Voicemail

SCAN_INTERVAL = timedelta(seconds=30)

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def _async_setup_services(hass: HomeAssistant, entry):

    entry_id = entry.entry_id
    name = entry.data[CONF_NAME]

    async def async_record(service_call):
        _LOGGER.debug("Service call: %s", service_call)
        raw_messages = service_call.data["messages"]
        messages = json_messages_to_list(raw_messages)

        voicemail: Voicemail = hass.data[DOMAIN][entry_id][VOICEMAIL_INSTANCE]
        await voicemail.async_record(messages)

    async def async_record_when(service_call):
        _LOGGER.debug("Service call: %s", service_call)

        condition = service_call.data.get(ATTR_CONDITION)
        raw_messages = service_call.data["messages"]
        messages = json_messages_to_list(raw_messages)

        _LOGGER.debug("%s was called with: %s", name, raw_messages)

        voicemail: Voicemail = hass.data[DOMAIN][entry_id][VOICEMAIL_INSTANCE]
        await voicemail.async_record_when(condition, messages)

    async def async_play_all(service_call):
        _LOGGER.debug("Service call: %s", service_call)
        voicemail: Voicemail = hass.data[DOMAIN][entry_id][VOICEMAIL_INSTANCE]
        await voicemail.async_play_all()

    hass.services.async_register(
        DOMAIN, f"{name}_record", async_record, SERVICE_RECORD_SCHEMA
    )

    hass.services.async_register(
        DOMAIN, f"{name}_record_when", async_record_when, SERVICE_RECORD_WHEN_SCHEMA
    )

    hass.services.async_register(DOMAIN, f"{name}_play_all", async_play_all)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""

    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {}

    voicemail = Voicemail(hass, entry)
    await voicemail.async_setup()

    data = {
        VOICEMAIL_INSTANCE: voicemail,
    }
    hass.data[DOMAIN][entry.entry_id] = data
    await _async_setup_services(hass, entry)

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    entry.add_update_listener(async_reload_entry)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if not unload_ok:
        return False

    name = entry.data[CONF_NAME]
    hass.data[DOMAIN].pop(entry.entry_id)
    hass.services.async_remove(DOMAIN, f"{name}_play_all")
    hass.services.async_remove(DOMAIN, f"{name}_record_when")

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
